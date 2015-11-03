from flask import Flask
import requests
import logging
import os

logging.basicConfig(level='DEBUG')

tmpl = '<html><head></head><body><pre>{}</pre></body></html>'
upstream = None
app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route('/cookie')
def cookie():
    res = requests.get(upstream)
    fortune = res.json()['fortune']
    return tmpl.format(fortune)


def run(app):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()


if __name__ == '__main__':
    upstream = os.environ['FORTUNE']
    run(app)
