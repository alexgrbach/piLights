import os
import stat
import math
import time
import pistrip as strip

from threading import Timer,Thread,Event
from sys import exit
from random import randint

try:
    from flask import Flask, render_template, json
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

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/pixel/get/<id>')
def getPixelColor(id):
	data = []
	data.append(strip.ColorToRGB(strip.get_pixel(int(id))))
	response = app.response_class(
	    response=json.dumps(data),
	    status=200,
	    mimetype='application/json'
	)
	return response

@app.route('/pixels/get/all')
def getPixelColors():
	data = []
	for x in range(1,strip.length()):
		data.append(strip.ColorToRGB(strip.get_pixel(x)))

	response = app.response_class(
	    response=json.dumps(data),
	    status=200,
	    mimetype='application/json'
	)
	return response

@app.route('/pixels/set/all/<r>/<g>/<b>')
def setPixelColors(r,g,b):
	strip.set_all_pixels(strip.Color(int(g),int(r),int(b)))
	strip.show()

	return getPixelColors()

@app.route('/pixel/set/<id>/<r>/<g>/<b>')
def setPixelColor(id,r,g,b):
	# we use bgr in this house
	strip.set_pixel(int(id), strip.Color(int(g),int(r),int(b)))
	strip.show()
	return getPixelColors()
	# return getPixelColor(id)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)