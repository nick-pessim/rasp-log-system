from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from add.routing import websocket_urlpatterns_add
from tcp_dump.routing import websocket_urlpatterns_tcp_dump

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns_add+
            websocket_urlpatterns_tcp_dump
        )
    )
})
