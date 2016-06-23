from flask import Flask
import random
import json
import logging

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('fortune')

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


#status_app = Flask(__name__ + '_status')

@app.route('/health')
def health():
    return 'ok'


@app.route('/quitquitquit', methods=['POST'])
def quit():
    logger.info('gotgotgot quitquitquit request')
    return 'ok'


@app.route('/abortabortabort', methods=['POST'])
def abort():
    logger.info('got abortabortabort request')
    return 'ok'


def run(app, port, status_port):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)

    #status_server = HTTPServer(WSGIContainer(status_app))
    #status_server.listen(status_port)

    IOLoop.instance().start()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fortunes')
    parser.add_argument('--port', default=8000)
    parser.add_argument('--status-port', default=8001)
    args = parser.parse_args()

    logger.info("Fortune app is starting")
    with open(args.fortunes, 'rb') as p:
        data = p.read().decode('utf-8', 'ignore')
        fortunes.extend(data.split('\n%\n'))

    run(app, args.port, args.status_port)
