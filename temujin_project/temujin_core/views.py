import json

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

from django.http import HttpResponse
from django.views.generic import View


from .models import NameSpace
from .helpers import instance_dict



class CreateNsView(View):
    model = NameSpace
    

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        try:
            ns = NameSpace.objects.get(name=name)
        except:
            ns = NameSpace.objects.create(name=name)

        data = json.dumps(instance_dict(ns))
        response_kwargs = {}
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)





#TODO: document
#TODO: handle errors

class BaseProcessView(View):

    http_method_names = ['get', 'post', 'options']
    
    inputs = {}
    outputs = {}
    parameters = {}

    def get(self, request, *args, **kwargs):
        """
        Returns a descriptor of view in json format
        """
        return self.render_descriptor(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)


    def get_namespace(self, request):
        ns = self.request.POST.get('__namespace__', None)
        if not ns:
            namespace = NameSpace.objects.create()
        else:
            namespace = NameSpace.objects.get(uuid=ns)

        return namespace.uuid


    def get_parameters(self, request):
        out = {}
        for parameter in self.parameters:
            try:
                out[parameter] = self.get_post_item(parameter)
            except:
                if 'required' in self.parameters[parameter] and not self.parameters[parameter]['required']:
                    out[parameter] = None 
                else:
                    raise ValueError("Missing parameter %s" % parameter)
        return out

    def get_inputs(self, request):
        out = {}
        for inputname in self.inputs:
            getter = getattr(self, 'get_input_' + inputname, None)
            if getter is not None:
                out[inputname] = getter(request)
            else:
                out[inputname] = self.get_post_item(inputname)
        return out

    
    def get_result(self, namespace, inputs, parameters):
        raise NotImplementedError


    def process(self, request, *args, **kwargs):
        parameters = self.get_parameters(request)
        inputs = self.get_inputs(request)
        namespace = self.get_namespace(request)
        result = self.get_result(request, namespace, inputs, parameters)
        return self.render_result(result)
    
    
    def get_descriptor(self):
        descriptor = {}
        descriptor['parameters'] = self.parameters
        descriptor['inputs'] = self.inputs
        descriptor['outputs'] = self.outputs
        return descriptor

    
    def get_post_item(self, parameter):
        return self.request.POST.get(parameter)



    def render_descriptor(self, request, *args, **kwargs):
        descriptor = self.get_descriptor()
        data = json.dumps(descriptor, cls=DjangoJSONEncoder)
        response_kwargs = {}
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def render_result(self, result):
        data = json.dumps(result, cls=DjangoJSONEncoder)
        response_kwargs = {}
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


from django.conf.urls import patterns, url


def register_process_view(viewClass, name):

    view_url = url(r'^process/'+ name + r"/$", viewClass.as_view(), name="process_%s" % name )

    return patterns('', view_url)


from django.conf import settings
BASE_FILE_PATH =settings.TEMUJIN_BASE_FILE_PATH

#@login_required
def serve_file(request, ns, filename):
    import os.path
    import mimetypes
    mimetypes.init()
    file_path = os.path.join(BASE_FILE_PATH, ns, filename)

    try:
        fsock = open(file_path,"r")
        #file = fsock.read()
        #fsock = open(file_path,"r").read()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print "file size is: " + str(file_size)
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])
        #response['Content-Disposition'] = 'attachment; filename=' + file_name            
    except IOError:
        raise
        response = HttpResponseNotFound()
    return response    
