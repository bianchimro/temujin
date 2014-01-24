from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temujin_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^temujin/', include('temujin_core.urls')),
    url(r'^console/', include('temujin_console.urls')),
    
)


from temujin_core.register import register_process_view
from temujin_image.views import ImageFilterView, ImageFilterViewSimpler

urlpatterns += register_process_view(ImageFilterView, 'image_filter');
urlpatterns += register_process_view(ImageFilterViewSimpler, 'image_filter_simpler');