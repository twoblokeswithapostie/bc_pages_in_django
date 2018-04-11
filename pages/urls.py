from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^update-pages/$', update_pages, name='update_pages'),
    url(r'^detail/(\d+)/$', detail, name='detail'),
]
