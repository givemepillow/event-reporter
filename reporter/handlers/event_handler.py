import os

import aiohttp
from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_apispec import request_schema, docs

from reporter.schemas import EventSchema
from reporter.utils import TextMessage, Message


class EventHandler(View):

    @docs(tags=['event'], responses={
        204: {"description": "OK. Message sent."},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    }, )
    @request_schema(EventSchema())
    async def post(self):
        data = await self.request.json()
        # message_text = TextMessage(title='Привет', text='Как дела?')
        # message = Message(chat_id=chat_id, message=message_text)
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #             f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
        #             data=message.json(),
        #             headers=self.headers) as response:
        #         try:
        #             assert response.status == 200
        #         except Exception:
        #             return web.Response(status=500)
        return web.Response(status=204)
