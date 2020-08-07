from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WidgetConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Set up a group for all clients called 'widgets'
        self.group_name = 'widgets'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def widget_save(self, event):
        # Send the message (event) to the clients
        await self.send_json({
            'model': 'widget',
            'action': 'save',
            'data': event['data']
        })
