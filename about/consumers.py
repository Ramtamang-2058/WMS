from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import DataR
from channels.db import database_sync_to_async


class TimeSeriesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to a specific channel group based on the chart ID
        self.chart_id = self.scope['url_route']['kwargs']['chart_id']
        self.group_name = f'chart_group_{self.chart_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send initial chart data to the connected client
        await self.send_initial_chart_data()

    async def disconnect(self, close_code):
        # Remove the consumer from the channel group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming data, e.g., update the chart
        pass

    @database_sync_to_async
    def get_chart_data(self):
        data = DataR.objects.filter(latitude=self.chart_id).values(
            'distance',
            'created_date'
        ).order_by('-id')[:10]

        chart_data = []
        for item in data:
            chart_data.append({
                'x': item['created_date'].strftime('%Y-%m-%dT%H:%M:%S'),
                'y': item['distance']
            })

        return chart_data

    async def send_initial_chart_data(self):
        chart_data = await self.get_chart_data()


        await self.send(json.dumps(chart_data))

    async def chart_update(self, event):
        # Send the updated chart data to the connected clients
        chart_id = event['chart_id']
        chart_data = await self.get_chart_data()

        await self.send(json.dumps(chart_data))
