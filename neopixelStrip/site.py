import os
import stat
import math
import time
import pistrip as strip
import atexit

from decimal import *
from threading import Timer,Thread,Event
from sys import exit
from random import randint
from collections import deque


try:
    from flask import Flask, render_template, json, request, jsonify, Response
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
t = perpetualTimer(1, default)
pixel_array = []


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/')
def home():
    pixel_data = []
    for x in range(0,strip.length()):
        pixel_data.append(strip.ColorToRGB(strip.get_pixel(x)))

    template = render_template('index.html', pixels=pixel_data)
    return template

@app.route('/off')
def off():
    global t
    t.cancel()
    global pixel_array
    pixel_array = []

    strip.off()
    return status()

def get_pixels():
    data = []
    for x in range(0,strip.length()):
        data.append(strip.ColorToRGB(strip.get_pixel(x)))
    return data

def build_response_data():
    data = {"app": "led_strip",
            "numberOfBulbs": strip.length(),
            "brightness": strip.get_brightness(),
            "stripColors": get_pixels()
            }
    return json.dumps(data)

@app.route('/status')
def status():
    data = build_response_data()
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/brightness/set/<value>')
def brightness_set(value):
    strip.set_brightness(int(value))
    strip.show()
    return 'ok'

@app.route('/pixel/set/array', methods = ['POST'])
def pixel_set_array():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            js = request.get_json()
            stripColors = js['stripColors']
            # print(stripColors)
            pixel_colors = []
            for i, color in enumerate(stripColors):
                pixel_colors.extend([obj_to_color(color)])
                strip.set_pixel(i, pixel_colors[i])
            strip.show()
            global pixel_array
            pixel_array = pixel_colors
        return status()
    return 400

@app.route('/pixel/shift/right/<delay>')
def pixel_shift_right(delay):
    global t
    t.cancel()
    def shift():
        global pixel_array
        pixel_array = shift_right(pixel_array)
        load_buffer_with_array(pixel_array)
        strip.show()

    t = perpetualTimer(float(delay), shift)
    t.start()
    return "ok"

@app.route('/pixel/shift/left/<delay>')
def pixel_shift_left(delay):
    global t
    t.cancel()
    def shift():
        global pixel_array
        pixel_array = shift_left(pixel_array)
        load_buffer_with_array(pixel_array)
        strip.show()

    t = perpetualTimer(float(delay), shift)
    t.start()
    return "ok"
##############################################################################
##                                                                          ##
##                             Animation stuff                              ##
##                                                                          ##
##############################################################################

def load_buffer_with_array(lst):
    for i, pixel in enumerate(lst):
        strip.set_pixel(i, pixel)

def shift_right(lst):
    lst = deque(lst)
    lst.rotate(1)
    return list(lst)

def shift_left(lst):
    lst = deque(lst)
    lst.rotate(-1)
    return list(lst)

##############################################################################
##                                                                          ##
##                             Response Helpers                             ##
##                                                                          ##
##############################################################################
def obj_to_color(data):
    return color(data[0], data[1], data[2]) 

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