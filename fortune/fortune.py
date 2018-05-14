import logging
import os
import random
from itertools import chain, repeat

from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('fortune')

READY_DELAY = int(os.getenv('READY_DELAY', 10))
fortunes = []
statuses = chain(repeat('running', READY_DELAY), repeat('ready'))

app = Flask(__name__)

Healthy = Gauge(
    'healthy', 'service healthchecks',
    ['name', 'actionable', 'dependentOn', 'type'])

healthchecks = [
    {
        'name': 'flow_emitter',
        'actionable': 'true',
        'dependentOn': '',
        'type': 'SELF'
    },
    {
        'name': 'phase_shifter',
        'actionable': 'true',
        'dependentOn': '',
        'type': 'SELF'
    },
    {
        'name': 'ouija',
        'actionable': 'false',
        'dependentOn': 'ghosts',
        'type': 'EXTERNAL_DEPENDENCY'
    },
]


@app.route('/')
def index():
    return 'ok'


@app.route('/fortune')
def fortune():
    return jsonify({
        "fortune": random.choice(fortunes)
    })


@app.route('/starbug-status')
def ready():
    return jsonify({'status': next(statuses)})


@app.route('/health')
def health():
    return 'ok'


@app.route('/metrics')
def metrics():
    for hc in healthchecks:
        Healthy.labels(**hc).set(0 if random.random() < 0.95 else 1)
    return Response(
        content_type=CONTENT_TYPE_LATEST,
        response=generate_latest(),
    )


@app.route('/service-metadata', methods=('GET',))
def monks_metadata():
    return jsonify({
        'service_name': 'fortune',
        'service_version': '1.0',
        'description': 'The fortune demo application',
        'owner': 'nobel'
    })


@app.route('/monks/healthcheck', methods=('GET',))
def monks_healthcheck():
    return jsonify({
        'healthy': [
            {
                'name': 'dummy-check',
                'type': 'SELF',
                'healthy': True,
                'actionable': True
            }
        ],
        'unhealthy': []
    })


@app.route('/quitquitquit', methods=['POST'])
def quit():
    logger.info('gotgotgot quitquitquit request')
    return 'ok'


@app.route('/abortabortabort', methods=['POST'])
def abort():
    logger.info('got abortabortabort request')
    return 'ok'


def run(app, port):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)

    IOLoop.instance().start()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fortunes')
    parser.add_argument('--port', default=8080)
    args = parser.parse_args()

    logger.info("Fortune app is starting")
    with open(args.fortunes, 'rb') as p:
        data = p.read().decode('utf-8', 'ignore')
        fortunes.extend(data.split('\n%\n'))

    run(app, args.port)
