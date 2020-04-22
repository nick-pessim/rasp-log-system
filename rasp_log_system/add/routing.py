from django.urls import re_path
from .consumers import OnlineRaspCheck

websocket_urlpatterns = [
    re_path(r'^ws/add/(?P<nome>[^/]+)/(?P<ip>[^/]+)/(?P<vers_snmp>[^/]+)/(?P<community>[^/]+)/$', OnlineRaspCheck),
]
