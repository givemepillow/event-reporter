import os
from typing import Optional
from uuid import UUID

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_apispec import request_schema, docs
from sqlalchemy import select

from reporter.db.base import Engine
from reporter.db.model import recipients
from reporter.schemas import EventSchema
from reporter.utils import TextMessage, Message


class EventHandler(View):
    headers = {
        'Content-Type': 'application/json'
    }
    db = Engine
    send_message_url = f"/bot{os.environ['BOT_TOKEN']}/sendMessage?parse_mode=HTML"

    @docs(tags=['event'], responses={
        204: {"description": "OK. Message sent."},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    }, )
    @request_schema(EventSchema())
    async def post(self):
        event = self.request.get('data')
        chat_id = await self.get_chat_id_by_token(event.get('token'))
        if not chat_id:
            return web.Response(status=401, text='Invalid token.')
        message_text = TextMessage(
            title=f"{self.type_emoji(event.get('type'))} {event.get('title')}",
            text=event.get('text'),
            dt=event.get('datetime')
        )
        message = Message(chat_id=chat_id, message=message_text)
        async with self.request.app['telegram_session'].post(
                self.send_message_url,
                data=message.json(),
                headers=self.headers
        ) as response:
            try:
                assert response.status == 200
            except Exception:
                return web.Response(status=500)
        return web.Response(status=204)

    async def get_chat_id_by_token(self, token: UUID) -> Optional[int]:
        async with self.db.connect() as c:
            token = (await c.execute(
                select(recipients.c.chat_id).where(recipients.c.token == token)
            )).scalar()
            return token

    @staticmethod
    def type_emoji(emoji_type: str):
        match emoji_type:
            case 'INFO':
                return ':information_source:'
            case 'WARNING':
                return ':warning:'
            case 'ERROR':
                return ':sos:'
            case _:
                raise ValueError("No matches.")
