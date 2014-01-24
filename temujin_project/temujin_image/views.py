import urllib, cStringIO
import os
from temujin_core.views import BaseProcessView, BaseTaskView

from temujin_core.helpers import generate_oid

from PIL import Image, ImageFilter

from django.core.urlresolvers import reverse
from django.conf import settings
BASE_FILE_PATH =settings.TEMUJIN_BASE_FILE_PATH


from temujin_core import websockets


from .tasks import process_image_test

class ImageFilterView(BaseProcessView):
    """
    this view turns an image into a bw one
    """

    outputs = {'image_url' : { 'type' : 'uri' }}
    arguments = { 
        'source_url' : { 'type' : 'uri' },
        'out_filename' : { 'type' : 'string', 'required' : True },
        'filter_name' : { 'type' : 'string', 'required' : True }
    }


    #dummy example of custom getter
    def get_arg_image_url(self, request):
        image_url  = self.get_post_item('source_url')
        return image_url


    def get_result(self, request, args):
        out = {}
        token = process_image_test.delay(args['source_url'], args['filter_name'], args['out_filename'])
        out['token'] = str(token)
        
        return out




#the same as above, simpler :)
class ImageFilterViewSimpler(BaseTaskView):
    outputs = {'image_url' : { 'type' : 'uri' }}
    arguments = { 
        'source_url' : { 'type' : 'uri' },
        'out_filename' : { 'type' : 'string', 'required' : True },
        'filter_name' : { 'type' : 'string', 'required' : True }
    }
    task = process_image_test
    task_arguments = ['source_url', 'filter_name', 'out_filename']
