import argparse
import os

from aiohttp import web

from reporter.app import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file', type=str, required=False)
    app = create_app(parser.parse_args())
    web.run_app(app, host='0.0.0.0', port=os.environ['PORT'])
