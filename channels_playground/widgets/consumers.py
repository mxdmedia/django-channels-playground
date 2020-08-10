from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer


class WidgetTextConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # Define the group_name 'widgets' which this Consumer will attach to.
        self.group_name = 'widgets'
        super().__init__(*args, **kwargs)

    async def connect(self):
        # Add this Consumer/Channel to the group `self.group_name`
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Remove this Consumer/Channel from the group `self.group_name` on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    # CRUD event handler.  Accessed from send commands via widget.crud
    async def widget_crud(self, event):
        # Send the message portion of the event data as a string to all subscribed clients
        await self.send(text_data=event['data']['message'])


class WidgetJsonConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # Define the group_name 'widgets' which this Consumer will attach to.
        self.group_name = 'widgets'
        super().__init__(*args, **kwargs)

    async def connect(self):
        # Add this Consumer/Channel to the group `self.group_name`
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Remove this Consumer/Channel from the group `self.group_name` on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    # CRUD event handler.  Accessed from send commands via widget.crud
    async def widget_crud(self, event):
        # Send the entire data dict from the event.  send_json automatically
        # encodes any dicts it is passed as json data.
        await self.send_json(event['data'])


class WidgetJsonDjangoAuthConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # Define the group_name 'widgets' which this Consumer will attach to.
        self.group_name = 'widgets'
        super().__init__(*args, **kwargs)

    async def connect(self):
        # if user is anyonymous reject the connection by closing with error code 4401.
        # 4401 is used, as there is no unauthorized error code in the websockets standard,
        # 4000-4999 are generic codes available to applications, and 401 is the http
        # error code for Unauthorized.
        if self.scope["user"].is_anonymous:
            await self.accept()
            await self.close(code=4401)
            return
        # Add this Consumer/Channel to the group `self.group_name`
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Remove this Consumer/Channel from the group `self.group_name` on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    # CRUD event handler.  Accessed from send commands via widget.crud
    async def widget_crud(self, event):
        # Send the entire data dict from the event.  send_json automatically
        # encodes any dicts it is passed as json data.
        await self.send_json(event['data'])
