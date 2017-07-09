#!/usr/bin/env python3

import os
import stat
import threading
import time
import edisonBulbs as bulbs
from sys import exit

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")


bulbs.setup()
app = Flask(__name__)

chan_list = list(bulbs.chan_list)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/all/off')
def alloff():
	bulbs.GPIO.output(chan_list, bulbs.GPIO.LOW)
	return "ok"

@app.route('/all/on/')
def allon():
	bulbs.GPIO.output(chan_list, bulbs.GPIO.HIGH)
	return "ok"

@app.route('/toggle/<bulb>')
def toggle(bulb):
	bulbs.toggle_bulb(chan_list[int(bulb)])
	# return "ok"
	return "ok"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)