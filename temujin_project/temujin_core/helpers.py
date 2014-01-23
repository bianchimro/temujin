import json
import uuid

from django.db.models.fields.related import ForeignKey

def generate_oid():
    return str(uuid.uuid4()).replace('-', '')


def instance_dict(instance, key_format=None):
    "Returns a dictionary containing field names and values for the given instance"
    
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()
        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
    return d

