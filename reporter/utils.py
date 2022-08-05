import datetime
import json

import emoji
from aiohttp import web


class TextMessage:
    def __init__(self, text: str, title: str = None, dt: datetime.datetime = None):
        if not text:
            raise ValueError("Empty message text!")
        self._title = title
        self._text = text
        self._datetime = dt

    def __str__(self):
        if self._title:
            _msg = f'''<b>{self._title}</b>\n\n<code>{self._text}</code>\n'''
        else:
            _msg = f'''{self._text}'''
        if self._datetime:
            _msg = _msg + f'''\n<i>{self._datetime.strftime("%Y/%m/%d %H:%M:%S")}</i>'''
        return _msg


class Message:
    def __init__(self, chat_id: int, message: TextMessage):
        self._message = {
            'chat_id': f'{chat_id}',
            'text': f'{message}'
        }

    def json(self):
        return json.dumps(self._message)


def json_response(
        status: int = 200, text_status: str = "ok", data: dict = None
) -> web.Response:
    return web.json_response(status=status, data={"data": data, "status": text_status})
