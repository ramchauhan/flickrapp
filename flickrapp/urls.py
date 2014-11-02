from django.conf.urls import patterns, include, url
from django.contrib import admin
from flickrphoto.views import get_all_photo, ajax_search_view, show_search_data
admin.autodiscover() 

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', get_all_photo, name='get_photo'),
    url(r'^search$', get_all_photo, name='get_photos'),
    url(r'^ajax_search$', ajax_search_view, name='get_next_images'),
    url(r'^show_data$', show_search_data, name='data_info'),
)
