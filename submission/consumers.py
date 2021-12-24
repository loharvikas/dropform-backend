from channels.generic.websocket import AsyncWebsocketConsumer
import json


class SubmissionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.form_id = self.scope["url_route"]["kwargs"]["formId"]
        self.group_name = "form_" + str(self.form_id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self):
        pass

    async def send_submission(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
