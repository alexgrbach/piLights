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

##############################################################################
##                                                                          ##
##                                 WebStuff                                 ##
##                                                                          ##
##############################################################################

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/pixel/get/<pixel>')
def get_pixel_color(pixel):
	data = []
	data.append(strip.ColorToRGB(strip.get_pixel(int(pixel))))
	response = app.response_class(
	    response=json.dumps(data),
	    status=200,
	    mimetype='application/json'
	)
	return response

@app.route('/pixels/get/all')
def get_pixel_colors():
	data = []
	for x in range(1,strip.length()):
		data.append(strip.ColorToRGB(strip.get_pixel(x)))

	response = app.response_class(
	    response=json.dumps(data),
	    status=200,
	    mimetype='application/json'
	)
	return response

@app.route('/set/pixel/all/<r>/<g>/<b>')
def set_pixel_all(r,g,b):
	strip.set_all_pixels(strip.Color(int(g),int(r),int(b)))
	strip.show()

	return get_pixel_colors()

@app.route('/set/pixel/range/<start_pixel>/<end_pixel>/<r>/<g>/<b>/')
def set_pixel_range(start_pixel,end_pixel,r,g,b):
	try:
		start = validate_int(start_pixel, 0, 299, "start")
		end = validate_int(end_pixel, 0, 299, "end")
		color = validate_color(r,g,b)
	except ValueError as e:
		return response("error", e.args)

	strip.set_pixel_range(start, end, color)
	strip.show()
	return get_pixel_colors()

@app.route('/set/pixel/<pixel>/<r>/<g>/<b>')
def set_pixel(pixel,r,g,b):
	# we use bgr in this house
	strip.set_pixel(int(pixel), strip.Color(int(g),int(r),int(b)))
	strip.show()
	return get_pixel_colors()

##############################################################################
##                                                                          ##
##                             Response Helpers                             ##
##                                                                          ##
##############################################################################

def response(response_type, data_object):
	data = {"app": "led_strip",
			"numberOfBulbs": strip.length(),
			}
	status_code = -1

	if response_type = "error":
		status_code = 400
		data.update({"Error" : {"Type" : "general", "Message" : data_object}})
	elif response_type = "validation_error"
		status_code = 400
		data.update({"Error" : {"Type" : "validation", "Message" : data_object}})
	else
		status_code = 200


	response = app.response_class(
	    response=json.dumps(data),
	    status=status_code,
	    mimetype='application/json'
	)
	return response

class response:
	"""docstring for response"""
	def __init__(self, arg):
		super(response, self).__init__()

		self.app_name = "neopixel_stirp"
		self.length = strip.length()
		self.status = ""
		self.status_code = 


		

##############################################################################
##                                                                          ##
##                                Validation                                ##
##                                                                          ##
##############################################################################

def validate_color(r,g,b):
	try:
		r = validate_int(r, 0, 255, "r")
		g = validate_int(g, 0, 255, "g")
		b = validate_int(b, 0, 255, "b")
	except ValueError:
		raise 

	return strip.Color(g,r,b)

def validate_int(input_int, minimum, maximum, friendly_name):
	try:
		valid_input = int(input_int)
	except ValueError:
		raise ValueError(friendly_name + 
						" must be a whole number"
						)

	if minimum < valid_input < maximum:
		raise ValueError(friendly_name + 
						' must be between ' + 
						minimum + 'and' + maximum
						)

	return valid_input


##############################################################################
##                                                                          ##
##                                App Start                                 ##
##                                                                          ##
##############################################################################

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)