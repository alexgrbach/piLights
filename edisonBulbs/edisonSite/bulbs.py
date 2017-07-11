#!/usr/bin/env python3

import os
import stat
from threading import Timer,Thread,Event
import time
import edisonBulbs as bulbs
from sys import exit
from flask import json
from random import randint

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def default():
    pass

bulbs.setup()
app = Flask(__name__)
channels = bulbs.channels
t = perpetualTimer(1,default)

@app.route('/status/')
def status():
	data = []
	for chan in channels:
		data.append(bulbs.GPIO.input(chan))
	response = app.response_class(
	    response=json.dumps(data),
	    status=200,
	    mimetype='application/json'
	)
	return response

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/all/off/')
def all_off():
	global t
	t.cancel()
	bulbs.GPIO.output(channels, bulbs.GPIO.LOW)
	return status()

@app.route('/all/on/')
def all_on():
	global t
	t.cancel()
	bulbs.GPIO.output(channels, bulbs.GPIO.HIGH)
	return status()

@app.route('/toggle/<bulb>')
def toggle(bulb):
	global t
	t.cancel()
	bulbs.toggle_bulb(channels[int(bulb)])
	return status()

@app.route('/routine/toggleRandomBulb/<delay>/')
def toggle_random_bulb(delay):
	def toggle_bulb():
		bulbs.toggle_bulb(channels[randint(0,7)])
		
	global t
	t.cancel()
	all_off()
	bulbs.toggle_random_bulbs()
	t = perpetualTimer(float(delay),toggle_bulb)
	t.start()
	return "ok"



@app.route('/routine/toggleRandomBulbs/<delay>/')
def toggle_random_bulbs(delay):
	global t
	t.cancel()
	all_off()
	bulbs.toggle_random_bulbs()
	t = perpetualTimer(float(delay),bulbs.toggle_random_bulbs)
	t.start()
	return "ok"



if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)