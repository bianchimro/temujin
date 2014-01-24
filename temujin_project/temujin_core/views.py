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
    
    arguments = {}
    outputs = {}

    def get(self, request, *args, **kwargs):
        """
        Returns a descriptor of view in json format
        """
        return self.render_descriptor(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        try:
            return self.process(request, *args, **kwargs)
        except Exception, e:
            return self.render_error(str(e))



    def get_args(self, request):

        out = {}
        for arg in self.arguments:
            getter = getattr(self, 'get_arg_' + arg, None)
            if getter is not None:
                out[arg] = getter(request)
            else:
                out[arg] = self.get_post_item(arg)
            
            if out[arg] is not None:
                continue
            else:
                if 'required' in self.arguments[arg] and not self.arguments[arg]['required']:
                    out[arg] = None 
                else:
                    raise ValueError("Missing argument %s" % arg)

        return out

    
    
    def get_result(self, args):
        raise NotImplementedError


    def process(self, request, *args, **kwargs):
        arguments = self.get_args(request)
        result = self.get_result(request, arguments)
        return self.render_result(result)

    
    def get_descriptor(self):
        descriptor = {}
        descriptor['args'] = self.arguments
        descriptor['outputs'] = self.outputs
        return descriptor

    
    def get_post_item(self, arg):
        return self.request.POST.get(arg)



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

    def render_error(self, error_string):
        error = {'error' : error_string }
        data = json.dumps(error, cls=DjangoJSONEncoder)
        response_kwargs = {}
        response_kwargs['content_type'] = 'application/json'
        response_kwargs['status'] = 500
        return HttpResponse(data, **response_kwargs)

class BaseTaskView(BaseProcessView):
    """
    this view turns an image into a bw one
    """

    #a celery task
    task = None
    #a list of task_arguments (from self.arguments)
    task_arguments = []
    #a list of task_kwarguments (from self.arguments)
    task_kwarguments = {}


    def get_result(self, request, args):
        if not self.task:
            raise ValueError("BaseTaskView has no task")
        out = {}
        #build up arguments
        t_args = []
        for task_arg in self.task_arguments:
            t_args.append(args[task_arg])

        t_kwargs = {}
        for task_kwarg in self.task_kwarguments:
            t_kwargs[task_kwarg] = args[task_kwarg]


        token = self.task.delay(*t_args, **t_kwargs)
        out['token'] = str(token)
        
        return out






######TODO: MOVE AWAY!
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
