import asyncio
import json
from django.contrib.sessions.models import Session
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
class TrafficConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'request_count',
            self.channel_name,
        )
        await self.accept()
        labels = []
        user_request_data = []
        non_user_request_data = []
        for i in range(5):
            now = timezone.localtime() - timezone.timedelta(minutes=5 - i)
            labels.append(now.strftime('%H:%M:%S'))
            user_request_count_i = len(Session.objects.filter(expire_date__gte=now, expire_date__lt=now + timezone.timedelta(minutes=1), 
                                                              session_key__contains='_auth_user_id',
            ))
            user_request_data.append(user_request_count_i)
            non_user_request_count_i = len(Session.objects.filter(
                expire_date__gte=now,
                expire_date__lt=now + timezone.timedelta(minutes=1),
                session_key__icontains='guest',
            ))
            non_user_request_data.append(non_user_request_count_i)
        request_count_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'User Requests',
                    'data': user_request_data,
                    'borderColor': 'rgb(255, 99, 132)',
                    'fill': False,
                },
                {
                    'label': 'Non-User Requests',
                    'data': non_user_request_data,
                    'borderColor': 'rgb(54, 162, 235)',
                    'fill': False,
                },
            ],
        }
        await self.send(text_data=json.dumps(request_count_data))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'request_count',
            self.channel_name,
        )

    async def update_request_count(self, event):
        """
        Receive request count update from TrafficMiddleware
        """
        request_count_data = event['request_count_data']
        await self.send(text_data=json.dumps(request_count_data))

    def get_request_count():
        now = timezone.localtime()
        last_five_minutes = now - timezone.timedelta(minutes=5)
        user_request_count = len(Session.objects.filter(
            expire_date__gte=last_five_minutes,
            session_key__contains='_auth_user_id',
            ))
        non_user_request_count = len(Session.objects.filter(
            expire_date__gte=last_five_minutes,
            session_key__icontains='guest',
            ))
        return user_request_count, non_user_request_count

    # async def send_request_count_data(self):
    #     """
    #     Send initial request count data to client
    #     """
        

    async def update_request_count_data(self):
        """
        Send updated request count data to clients every minute
        """
        while True:
            user_request_count, non_user_request_count = await self.get_request_count