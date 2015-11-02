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


if __name__ == '__main__':
    upstream = os.environ['FORTUNE']
    app.run(host='0.0.0.0', port=8000)
