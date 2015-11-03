from flask import Flask
import random
import json
import logging

logging.basicConfig(level='DEBUG')

fortunes = []

app = Flask(__name__)

@app.route('/')
def index():
    return 'ok'


@app.route('/fortune')
def fortune():
    return json.dumps({
        "fortune": random.choice(fortunes)
    })


def run(app):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fortunes')
    args = parser.parse_args()
    with open(args.fortunes, 'rb') as p:
        data = p.read().decode('utf-8', 'ignore')
        fortunes.extend(data.split('\n%\n'))

    run(app)
