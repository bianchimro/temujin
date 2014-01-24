from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


import urllib, cStringIO
import os
from PIL import Image, ImageFilter

from django.core.urlresolvers import reverse
from django.conf import settings
BASE_FILE_PATH =settings.TEMUJIN_BASE_FILE_PATH


from temujin_core import websockets
from temujin_core.task_helpers import WebSocketExceptionTask



#TODO:ns should be automatic
def get_file_resource(name):
    out = {}
    ns = 'x'
    target_path = os.path.join(BASE_FILE_PATH, ns)
    if not os.path.isdir(target_path):
        os.mkdir(target_path)
    out['filename'] = os.path.join(target_path, name)
    out['url'] = reverse('temujin_serve_file', kwargs={'ns':ns, 'filename':name})
    return out



def proc_image_example(source_url, filter_name, name):
    image_file = cStringIO.StringIO(urllib.urlopen(source_url).read())
    img = Image.open(image_file)
    func = getattr(ImageFilter, filter_name)
    img = img.filter(func)
    destination = get_file_resource(name)
    img.save(destination['filename'])
    return destination['url']



@task(bind=True, base=WebSocketExceptionTask)
def process_image_test(self, source_url, filter_name, name):
    out = {}
    out['token'] = str(self.request.id)
    out['url'] = proc_image_example(source_url, filter_name, name)
    return out