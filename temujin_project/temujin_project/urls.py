from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from temujin_console.views import ConsoleView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temujin_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^temujin/', include('temujin_core.urls')),
    url(r'^$', ConsoleView.as_view(), name='console'),
)


from temujin_core.views import register_process_view
from temujin_image.views import ImageFilterView

urlpatterns += register_process_view(ImageFilterView, 'image_filter')

