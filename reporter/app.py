import logging
import os
from argparse import Namespace

import aiohttp
from aiohttp import web
from aiohttp.abc import Application
from dotenv import load_dotenv

from reporter.handlers import HANDLERS


def setup_logging(app: web.Application) -> None:
    logging.basicConfig(level=logging.DEBUG)
    app.logger = logging.getLogger(__name__)


async def set_webhook(app: web.Application):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/setWebhook",
                data={"url": f"https://{os.environ['DOMAIN_NAME']}/"},
                headers={'Content-Type': 'application/json'}
        ) as response:
            app.logger.debug(f'Set webhook status: {response.status}.')
            assert response.status == 200


def create_app(args: Namespace) -> Application:
    if args.env_file:
        load_dotenv(dotenv_path=args.env_file)
    app = web.Application()
    setup_logging(app)
    app.on_startup.append(set_webhook)
    for handler in HANDLERS:
        app.logger.debug('Registering handler %r as %r', handler, handler.URL_PATH)
        app.router.add_view(handler.URL_PATH, handler)
    return app
