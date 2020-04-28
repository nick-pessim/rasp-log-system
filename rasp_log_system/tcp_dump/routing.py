from django.urls import re_path
from .consumers import tcp_dump_request

websocket_urlpatterns_tcp_dump = [
    re_path(r'^ws/tcp-dump/(?P<nome>[^/]+)/(?P<senha>[^/]+)/(?P<ip>[^/]+)/(?P<interface>[^/]+)/(?P<duracao>[^/]+)/$', tcp_dump_request),
]
