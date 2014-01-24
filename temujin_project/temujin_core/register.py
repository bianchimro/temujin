from django.conf.urls import patterns, url


def register_process_view(viewClass, name):

    view_url = url(r'^process/'+ name + r"/$", viewClass.as_view(), name="process_%s" % name )

    return patterns('', view_url)
