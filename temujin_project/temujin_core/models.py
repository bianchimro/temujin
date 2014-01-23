from django.db import models
import uuid



def generate_uuid():
    return str(uuid.uuid1())



class NameSpace(models.Model):
    name = models.CharField(max_length=64, default='', null=True, blank=True )
    uuid = models.CharField(max_length=64, default=generate_uuid)



