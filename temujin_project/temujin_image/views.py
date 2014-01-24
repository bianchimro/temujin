import urllib, cStringIO
import os
from temujin_core.views import BaseProcessView

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

    inputs = {'image_url' : { 'type' : 'uri' }}
    outputs = {'image_url' : { 'type' : 'uri' }}
    parameters = { 
        'out_filename' : { 'type' : 'string', 'required' : True },
        'filter' : { 'type' : 'string', 'required' : True }
    }


    #dummy example of custom getter
    def get_input_image_url(self, request):
        image_url  = self.get_post_item('image_url')
        return image_url


    def get_result(self, request, inputs, parameters):
        out = {}

        source_url = inputs['image_url']
        token = process_image_test.delay(source_url, parameters['filter'], parameters['out_filename'])
        out['token'] = str(token)
        
        return out





