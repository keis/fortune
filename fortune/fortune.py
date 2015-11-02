from flask import Flask
import random
import json
import logging

logging.basicConfig(level='DEBUG')

fortunes = []

app = Flask(__name__)

@app.route('/')
def fortune():
    return json.dumps({
        "fortune": random.choice(fortunes)
    })


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fortunes')
    args = parser.parse_args()
    with open(args.fortunes, 'rb') as p:
        data = p.read().decode('utf-8', 'ignore')
        fortunes.extend(data.split('\n%\n'))
    app.run(host='0.0.0.0', port=8000)
