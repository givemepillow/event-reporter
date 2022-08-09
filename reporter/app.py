import logging
import os
from argparse import Namespace

import aiohttp
from aiohttp import web
from aiohttp.abc import Application
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from dotenv import load_dotenv

from reporter.handlers import MessageHandler, EventHandler
from reporter.middlewares import error_middleware


def setup_logging(app: web.Application) -> None:
    logging.basicConfig(level=logging.DEBUG)
    app.logger = logging.getLogger(__name__)


async def set_webhook(app: web.Application):
    async with app['telegram_session'].post(
            f"/bot{os.environ['BOT_TOKEN']}/setWebhook",
            json={"url": f"https://{os.environ['DOMAIN_NAME']}{os.environ['WEBHOOK_PATH']}"},
            headers={'Content-Type': 'application/json'}
    ) as response:
        app.logger.debug(f'Set webhook status: {response.status}.')
        assert response.status == 200


async def telegram_session_ctx(app: web.Application) -> None:
    app['telegram_session'] = aiohttp.ClientSession(f"https://api.telegram.org")
    yield
    await app['telegram_session'].close()


def create_app(args: Namespace) -> Application:
    if args.env_file:
        load_dotenv(dotenv_path=args.env_file)
    app = web.Application()
    setup_logging(app)

    app.cleanup_ctx.extend((telegram_session_ctx,))
    app.on_startup.append(set_webhook)

    app.router.add_view(os.environ['WEBHOOK_PATH'], MessageHandler)
    app.router.add_view('/event', EventHandler)

    app.middlewares.append(validation_middleware)
    app.middlewares.append(error_middleware)

    setup_aiohttp_apispec(
        app=app,
        title="API REFERENCE",
        version="v1",
        url="/swagger.json",
        swagger_path="/swagger"
    )

    return app
