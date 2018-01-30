import os
import stat
import math
import time
import pistrip as strip
import atexit

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
	pixel_data = []
	for x in range(0,strip.length()):
		pixel_data.append(color_to_hex(strip.get_pixel(x)))

	return render_template('index.html', pixels=pixel_data)

@app.route('/off')
def off():
	strip.off()
	return pixel_get_all()

@app.route('/pixel/get/<pixel>')
def pixel_get(pixel):
	data = []
	data.append(strip.ColorToRGB(strip.get_pixel(int(pixel))))
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/pixel/get/all')
def pixel_get_all():
	response_object = {"app": "led_strip",
			"numberOfBulbs": strip.length(),
			"brightness": strip.get_brightness()
			}

	pixel_data = []
	for x in range(0,strip.length()):
		pixel_data.append(color_to_hex(strip.get_pixel(x)))
	response_object.update({"stripColors": pixel_data})

	# html_data = []
	# for index, html_color in enumerate(pixel_data):
	# 	html_data.append(color_to_icon(index, html_color))

	# response_object.update({"stripHTML": html_data})

	response = app.response_class(
		response=json.dumps(response_object),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/status')
def status():
	return pixel_get_all()

@app.route('/brightness/set/<value>')
def brightness_set(value):
	strip.set_brightness(int(value))
	strip.show()
	return 'ok'

@app.route('/brightness/get')
def brightness_get():
	response = app.response_class(
		response=json.dumps(strip.get_brightness()),
		status=200,
		mimetype='application/json'
	)
	return response 

@app.route('/pixel/set/all/<r>/<g>/<b>')
def pixel_set_all(r,g,b):
	strip.set_all_pixels(color(r,g,b))
	strip.show()
	return pixel_get_all()

@app.route('/pixel/set/range/<start_pixel>/<end_pixel>/<r>/<g>/<b>/')
def pixel_set_range(start_pixel,end_pixel,r,g,b):
	# try:
	# 	start = int(validate_int(start_pixel, 0, 299, "start"))
	# 	end = int(validate_int(end_pixel, 0, 299, "end"))
	# 	color = validate_color(r,g,b)
	# except ValueError as e:
	# 	return response("error", e.args)
	# print("site.py pixel_set_range")
	# print("start_pixel: " + start_pixel + " end_pixel: " + end_pixel)
	strip.set_pixel_range(int(start_pixel), int(end_pixel), color(r,g,b))
	strip.show()
	# return "ok"
	return pixel_get_all()

@app.route('/pixel/set/single/<pixel>/<r>/<g>/<b>')
def pixel_set(pixel,r,g,b):
	# we use bgr in this house
	strip.set_pixel(int(pixel), color(r,g,b))
	strip.show()
	return pixel_get_all()

##############################################################################
##                                                                          ##
##                             Response Helpers                             ##
##                                                                          ##
##############################################################################

def color(r,g,b):
	return strip.Color(int(g),int(r),int(b))

def response(response_type, data_object):
	data = {"app": "led_strip",
			"numberOfBulbs": strip.length(),
			}
	status_code = -1

	if response_type == "error":
		status_code = 400
		data.update({"Error" : {"Type" : "general", "Message" : data_object}})
	elif response_type == "validation_error":
		status_code = 400
		data.update({"Error" : {"Type" : "validation", "Message" : data_object}})
	else:
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
		super(self, object).__init__()

		self.app_name = "neopixel_stirp"
		self.length = strip.length()
		self.status = ""
		self.status_code = ""

def color_to_icon(index, html_color):
	return """<i class="fas fa-circle" index=\"""" + str(index) + """\" style="color:""" + html_color + """"></i>"""
	 

def color_to_hex(pixel_color):
	return '#%02x%02x%02x' % strip.ColorToRGB(pixel_color)		

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

	return color(g,r,b)

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