#!/usr/bin/env python3

import argparse
import logging
from flask import Flask, request
from turbo_parser_server import TurboParserServer

logger = logging.getLogger('TurboParserServer')
logger.setLevel(logging.INFO)

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Start TurboParser Server.')
parser.add_argument('-lang', default='english', help='Language')
parser.add_argument('-annotators', default='lemma, morph, pos, ner, parse, coref, sem', help='Annotators to load')
parser.add_argument('-threads', type=int, default=16, help='Number of threads to use.')
parser.add_argument('-models_path', default='/models/', help='Path to TurboParser models')

args = parser.parse_args()

# load TurboPaser
logger.info('Loading TurboParser...')
server = TurboParserServer(language=args.lang, data_path=args.models_path, annotators=args.annotators)

@app.route('/', methods=['POST', 'GET'])
def index():
    # en es
    logger.debug('Received request: {}'.format(request.headers['Content-Type']))
    language = request.args.get('lang', 'en')
    annotators = request.args.get('annotators', '')
    if request.headers['Content-Type'] == 'text/plain':
        return server.parse(request.data.decode('utf8'), language, annotators)
    else:
        logger.error('Request headers should be "text/plain"')

if __name__ == "__main__":
    logger.info('Application loaded. Read to receive connections.')
    app.run(debug=True, host='0.0.0.0', port=5000, processes=args.threads, use_reloader=False)
