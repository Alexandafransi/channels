import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NoseyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("gossip", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, code):
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print(f"Remove {self.channel_name} channel from gossip")

    async def user_gossip(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

    async def food_gossip(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
    # while 1:
    #     await asyncio.sleep(1)
    #     await self.send_json("tick")
    #     await asyncio.sleep(1)
    #     await self.send_json("......tock")

# from channels.consumer import AsyncConsumer
#
#
# class EchoConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         await self.send({
#             "type": "websocket.accept",
#         })
#
#     async def websocket_receive(self, event):
#         await self.send({
#             "type": "websocket.send",
#             "text": event["text"],
#         })
