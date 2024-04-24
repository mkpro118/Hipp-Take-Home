from flask import Flask, request, render_template
from flask_cors import CORS
from typing import Callable, Sequence

import argparse
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


def styles(self):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVER_PORT', 5000))
    debug = bool(os.environ.get('FLASK_DEBUG', True))

    ps_host = os.environ.get('PROXYSERVER_HOST', 'localhost')
    ps_port = os.environ.get('PROXYSERVER_PORT', 8000)

    parser.add_argument('-fh', '--flask-hostname', type=str, default=host)
    parser.add_argument('-fp', '--flask-port', type=int, default=port)
    parser.add_argument('-fd', '--flask-debug',
                        action='store_true', default=debug)

    args = parser.parse_args()

    host = args.flask_hostname
    port = args.flask_port
    debug = args.flask_debug

    app.run(host=host, port=port, debug=debug)
