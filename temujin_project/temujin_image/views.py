import urllib, cStringIO
import os
from temujin_core.views import BaseProcessView

from temujin_core.helpers import generate_oid

from PIL import Image, ImageFilter

from django.core.urlresolvers import reverse
from django.conf import settings
BASE_FILE_PATH =settings.TEMUJIN_BASE_FILE_PATH


def get_file_resource(ns, name=None, extension=None):
    oid = generate_oid()
    if not name:
        filename = oid + "." + extension
    else:
        filename = name

    target_path = os.path.join(BASE_FILE_PATH, ns)
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    out = {}
    out['filename'] = os.path.join(target_path, filename)
    out['url'] = reverse('temujin_serve_file', kwargs={'ns':ns, 'filename':filename})
    return out



def proc_image_example(source_url, filter, namespace, name=None):
    image_file = cStringIO.StringIO(urllib.urlopen(source_url).read())
    img = Image.open(image_file)
    
    func = getattr(ImageFilter, filter)
    img = img.filter(func)
    destination = get_file_resource(namespace, name=name, extension="jpg")
    img.save(destination['filename'])
    return destination['url']




class ImageFilterView(BaseProcessView):
    """
    this view turns an image into a bw one
    """

    inputs = {'image_url' : { 'type' : 'uri' }}
    outputs = {'image_url' : { 'type' : 'uri' }}
    parameters = { 
        'out_filename' : { 'type' : 'string', 'required' : False },
        'filter' : { 'type' : 'string', 'required' : True }
    }


    def get_input_image_url(self, request):
        image_url  = self.get_post_item('image_url')
        return image_url

    def get_result(self, request, namespace, inputs, parameters):
        out = {}

        source_url = inputs['image_url']
        out_url = proc_image_example(source_url, parameters['filter'], namespace, name=parameters['out_filename'])
        
        #todo: this should be done by a worker.
        out['image_url'] = out_url

        return out





