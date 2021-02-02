# chat/routing.py
from django.urls import re_path
# from channels.routing import route
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/wd/game/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/wd/websocket.receive/$', consumers.ws_receive),
    # re_path(r'ws/wd/websocket.connect/$', consumers.ws_connect),
    # re_path(r'ws/wd/websocket.disconnect/$', consumers.ws_disconnect),
    
]

# channel_routing = [
#   route("websocket.receive", ws_receive, path=r"^/websockets/$"),
#   route("websocket.connect", ws_connect, path=r"^/websockets/$"),
# ]

