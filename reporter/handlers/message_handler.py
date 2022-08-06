import os
from uuid import uuid1, UUID

import aiohttp
from aiohttp import web
from aiohttp.web_urldispatcher import View
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert

from reporter.db.base import Engine
from reporter.db.model import recipients
from reporter.utils import TextMessage, Message


class MessageHandler(View):
    headers = {
        'Content-Type': 'application/json'
    }
    engine = Engine

    async def post(self):
        data = await self.request.json()
        chat_id = data['message']['chat']['id']
        content = data['message']['text']
        answer = await self.handle(content, chat_id)
        message = Message(chat_id=chat_id, message=answer)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage?parse_mode=HTML",
                    data=message.json(),
                    headers=self.headers) as response:
                try:
                    assert response.status == 200
                except Exception:
                    return web.Response(status=500)
        return web.Response(status=200)

    async def handle(self, content: str, chat_id: int) -> TextMessage:
        match content:
            case '/start':
                token = f"\n<code>{await self.start(chat_id)}</code>"
                return TextMessage(f'Ваш токен для доступа к API: {token}')
            case '/delete':
                await self.delete(chat_id)
                return TextMessage('Токен безвозвратно удалён, если хотите создать новый - введите: /start.')
            case '/refresh':
                token = f"\n<code>{await self.refresh(chat_id)}</code>"
                return TextMessage(f'Ваш новый токен для доступа к API: {token}')
            case _:
                return TextMessage('Чего-чего? Попробуйте заглянуть в меню бота.')

    async def start(self, chat_id: int) -> UUID:
        async with self.engine.connect() as c:
            async with c.begin():
                token = (await c.execute(
                    select(recipients.c.token).where(recipients.c.chat_id == chat_id)
                )).scalar()
                if token:
                    return token
                token = uuid1()
                await c.execute(
                    insert(recipients).values({
                        'chat_id': chat_id,
                        'token': token
                    })
                )
                return token

    async def delete(self, chat_id: int):
        async with self.engine.connect() as c:
            async with c.begin():
                await c.execute(
                    delete(recipients).where(recipients.c.chat_id == chat_id)
                )

    async def refresh(self, chat_id: int) -> UUID:
        async with self.engine.connect() as c:
            async with c.begin():
                token = uuid1()
                await c.execute(
                    update(recipients).values({
                        'chat_id': chat_id,
                        'token': token
                    })
                )
                return token
