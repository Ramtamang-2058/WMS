from django.urls import re_path

from about.consumers import TrafficConsumer
websocket_urlpatterns = [
    re_path(r'ws/user_traffic/$', TrafficConsumer.as_asgi()),
]