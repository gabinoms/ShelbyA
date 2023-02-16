from flask import Flask, request
from threading import Thread

app = Flask('__name__')

def run():
	from waitress import serve
	serve(app, host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()
