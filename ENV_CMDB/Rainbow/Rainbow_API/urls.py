from django.conf.urls import url
from Rainbow_API.views import *

urlpatterns = [
    url(r'^server/$', ServerDetail.as_view(), name = 'server'),
    url(r'^memory/$', MemoryDetail.as_view(), name = 'memory'),
    url(r'^disk/$', DiskDetail.as_view(), name = 'disk'),
    url(r'^cpu/$', CPUDetail.as_view(), name = 'cpu'),
]
