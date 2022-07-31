import os

import aiohttp
from aiohttp import web
from aiohttp.web_urldispatcher import View

from reporter.utils import TextMessage, Message


class MessageHandler(View):
    URL_PATH = os.environ['WEBHOOK_PATH']
    headers = {
        'Content-Type': 'application/json'
    }

    async def post(self):
        data = await self.request.json()
        chat_id = data['message']['chat']['id']
        content = data['message']['text']

        message_text = TextMessage(title='Привет', text='Как дела?')
        message = Message(chat_id=chat_id, message=message_text)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
                    data=message.json(),
                    headers=self.headers) as response:
                try:
                    assert response.status == 200
                except Exception:
                    return web.Response(status=500)
        return web.Response(status=200)
