import json


class TextMessage:
    def __init__(self, title: str, text: str):
        if not text:
            raise ValueError("Empty message text!")
        self._title = title or ''
        self._text = text

    def __str__(self):
        if self._title:
            return self._title + '\n' + self._text
        return self._text


class Message:
    def __init__(self, chat_id: int, message: TextMessage):
        self._message = {
            'chat_id': f'{chat_id}',
            'text': f'{message}'
        }

    def json(self):
        return json.dumps(self._message)
