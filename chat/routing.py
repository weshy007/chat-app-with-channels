from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"talk/(?P<room_id>\w+)/$", consumers.TalkConsumer.as_asgi()),
]