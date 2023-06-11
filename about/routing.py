from django.urls import re_path
from .consumers import TimeSeriesConsumer

websocket_urlpatterns = [
    re_path(r'ws/data/(?P<chart_id>[\d.]+)/$', TimeSeriesConsumer.as_asgi()),
]
