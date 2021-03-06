'''
To run:
python register.py test_filename.json

App will display the url students should send their post requests to.
'''


from flask import Flask, request
import flask_restful as restful
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import sys
import requests
import simplejson
import random
import pytz
from threading import Thread
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import pandas as pd
import socket
import logging
logging.basicConfig()

PORT = 5000
IP = socket.gethostbyname('localhost')
URLS = set()
REGISTER = 'register'
SCORE = 'score'
APP = None


def load_data(filename, label='acct_type'):
    data = pd.read_json(filename)
    #data.drop(label, axis=1, inplace=True)
    return data

def start_server():
    print("Starting server...")
    app = Flask(__name__)
    api = restful.Api(app)
    api.add_resource(Register, f'/{REGISTER}')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT, '0.0.0.0')
    thread = Thread(target=IOLoop.instance().start)
    thread.start()
    url = 'http://{0}:{1}/{2}'.format(IP, PORT, REGISTER)
    print(f"Server started. Listening for posts at: {url}")
    return app

def get_random_datapoint():
    index = random.randint(0, len(DATA))
    datapoint = DATA.loc[[index]].to_dict()
    # fix the formatting
    for key, value in datapoint.iteritems():
        datapoint[key] = value.values()[0]
    return index, datapoint

def ping():
    global APP
    if not APP:
        APP = start_server()

    index, datapoint = get_random_datapoint()
    print(f"Sending datapoint {index} to {len(URLS)} urls")

    to_remove = []

    for url in URLS:
        headers = {'Content-Type': 'application/json'}
        try:
            requests.post('{0}/{1}'.format(url, SCORE),
                          data=simplejson.dumps(datapoint),
                          headers=headers)
            print(f"{url} sent data.")
        except requests.ConnectionError as e:
            print(f"{url} not listening. Removing...")
            to_remove.append(url)

    for url in to_remove:
        URLS.remove(url)


class Register(restful.Resource):
    def post(self):
        ip = request.form['ip']
        port = request.form['port']
        url = 'http://{0}:{1}'.format(ip, port)
        if url in URLS:
            print(f"{url} already registered")
        else:
            URLS.add(url)
            print(f"{url} is now registered")
        return {'Message': 'Added url {0}'.format(url)}

    def put(self):
        return simplejson.dumps(request.json)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python register.py test_filename.json")
        #exit()
    print("It can take up to 30 seconds to start.")
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"Invalid filename: {filename}")
        print("Goodbye.")
        #exit()

    print("Starting scheduler...")
    scheduler = BlockingScheduler(timezone=pytz.utc)
    scheduler.add_job(ping, 'interval', seconds=10, max_instances=100)

    print("Loading data...")
    DATA = load_data(filename)

    print("Press Ctrl+C to exit")
    try:
        scheduler.start()
    except KeyboardInterrupt as SystemExit:
        print("Goodbye!")
