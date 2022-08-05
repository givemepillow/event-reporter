# event-reporter

REST API service that allows send report messages to telegram via a bot.

Bot (here you can get a token and use the API): [REPORTER ✉](https://t.me/EventReporterBot)

Working service: [event-reporter.droptheseas.ru](https://event-reporter.droptheseas.ru)

API:
> **POST** `/event`
> 
> **body:**
> ```json
> {
>   "datetime": "2022-08-08T13:00:00.000Z",
>   "type": "INFO",
>   "title": "Заголовок, что-то да означающий.",
>   "text": "Сообщение со смыслом.",
>   "token": "c69ee156-14c8-11ed-956c-b0000adbc8e6"
> }
> ```
> **types:** `INFO, WARNING, ERROR`

