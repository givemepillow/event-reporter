import os

import aiohttp
from aiohttp import web
from aiohttp.web_urldispatcher import View

from reporter.utils import TextMessage, Message


class MessageHandler(View):
    headers = {
        'Content-Type': 'application/json'
    }

    async def post(self):
        data = await self.request.json()
        chat_id = data['message']['chat']['id']
        content = data['message']['text']
        answer = await self.handle(content)
        message = Message(chat_id=chat_id, message=answer)
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

    async def handle(self, text: str) -> TextMessage:
        match text:
            case '/start':
                TextMessage('Вы нажали старт.')
            case '/delete':
                TextMessage('Вы нажали удалить.')
            case '/refresh':
                TextMessage('Вы нажали обновить.')
            case _:
                return TextMessage('Не понял. Попробуйте заглянуть в меню бота.')
