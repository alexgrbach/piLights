import time
import pistrip as strip
import os as sys
import math

from random import randint
from neopixel import *

def snakes(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
	fire_down(width, delay, brightness, color)
	fire_back(width, delay, brightness, color)

def fire_down(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
	strip.brightness(brightness)
	for x in range(-width, strip.length(),1):
		for y in range(width):
			if(x+y >= 0):
				strip.set_pixel(x+y, color)
		strip.show()
		time.sleep(delay)
		strip.clear()

def fire_back(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
	strip.brightness(brightness)
	for x in range(strip.length(), -width, -1):
		for y in range(width):
			if(x+y >= 0):	
				strip.set_pixel(x+y, color)
			#print "x: %s y: %s" %(x,y)
		strip.show()
		time.sleep(delay)
		strip.clear()

def random_snakes():
	short_snake = 5
	long_snake = 40
	width = randint(short_snake, long_snake)
	delay = 0
	brightness = 255
	color = strip.led_colors.random()
	fire_down_with_background(width, delay, brightness, color)
	fire_back_with_background(width, delay, brightness, color)

def fire_down_with_background(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
	strip.brightness(brightness)
	colors = [strip.led_colors.random(), strip.led_colors.random(), strip.led_colors.random(), strip.led_colors.random()]

	for x in range(-width, strip.length(),1):
		for y in range(10, 63, 1):
			strip.set_pixel(y, colors[0])
		for y in range(64, 142, 3):
			strip.set_pixel(y, colors[1])
		for y in range(143, 221, 3):
			strip.set_pixel(y, colors[2])
		for y in range(222, 299, 3):
			strip.set_pixel(y, colors[3])
		for y in range(width):
			if(x+y >= 0):
				strip.set_pixel(x+y, color)
		strip.show()
		time.sleep(delay)
		strip.clear()

def fire_back_with_background(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
	strip.brightness(brightness)
	colors = [strip.led_colors.random(), strip.led_colors.random(), strip.led_colors.random(), strip.led_colors.random()]
	for x in range(strip.length(), -width, -1):
		for y in range(10, 63, 1):
			strip.set_pixel(y, colors[0])
		for y in range(64, 142, 3):
			strip.set_pixel(y, colors[1])
		for y in range(143, 221, 3):
			strip.set_pixel(y, colors[2])
		for y in range(222, 299, 3):
			strip.set_pixel(y, colors[3])
		for y in range(width):
			if(x+y >= 0):	
				strip.set_pixel(x+y, color)
			#print "x: %s y: %s" %(x,y)
		strip.show()
		time.sleep(delay)
		strip.clear()




def breathe(step_width=5, min_brightness=60, max_brightness=255, color=strip.led_colors.get("White")):
	strip.set_all_pixels(color)
	for y in range(min_brightness, max_brightness, step_width):
			strip.brightness(y)
			strip.show()
	for y in range(max_brightness, min_brightness, -step_width):
		strip.brightness(y)
		strip.show()
	strip.clear()

def flash_all(delay=1, color=strip.led_colors.get("White")):
	strip.set_all_pixels(color)
	strip.show()
	time.sleep(delay)
	strip.off()
	time.sleep(0)

def lol():
	delay=0.1
	for x in range(0, strip.length(), 3):
		strip.set_pixel(x, strip.led_colors.get("Blue"))
		strip.set_pixel(x+1, strip.led_colors.get("Green"))
		strip.set_pixel(x+2, strip.led_colors.get("Red"))
	strip.show()
	time.sleep(delay)
	strip.clear()
	for x in range(0, strip.length(), 3):
		strip.set_pixel(x+1, strip.led_colors.get("Blue"))
		strip.set_pixel(x+2, strip.led_colors.get("Green"))
		strip.set_pixel(x, strip.led_colors.get("Red"))
	strip.show()
	time.sleep(delay)
	strip.clear()
	for x in range(0, strip.length(), 3):
		strip.set_pixel(x+2, strip.led_colors.get("Blue"))
		strip.set_pixel(x, strip.led_colors.get("Green"))
		strip.set_pixel(x+1, strip.led_colors.get("Red"))
	strip.show()
	time.sleep(delay)
	strip.clear()


def cycle_all_colors():
	color = strip.led_colors.cycle()
	#exclude black
	if(color == 0):
		color = strip.led_colors.cycle()
	return (color)

def rainbow(clock):
    offset = 0

    for x in range(strip.length()):
        r = 0
        g = 0
        r = (math.cos((x+clock)/2.0) + math.cos((1+clock)/2.0)) * 64.0 + 128.0
        g = (math.sin((x+clock)/1.5) + math.sin((1+clock)/2.0)) * 64.0 + 128.0
        b = (math.sin((x+clock)/2.0) + math.cos((1+clock)/1.5)) * 64.0 + 128.0
        r = max(0, min(255, r + offset))
        g = max(0, min(255, g + offset))
        b = max(0, min(255, b + offset))
        strip.set_pixel(x,Color(int(r),int(g),int(b)))
    strip.show()

print("Testing...")
i = 0.0
strip.brightness(100)
try:
	
	#print(strip.length())
	while True:
		#breathe(3, 60, 255, strip.led_colors.random())
		#flash_all(.1, cycle_all_colors())
		#fire_down(1,0,255,cycle_all_colors())
		#lol()
		#print(strip.led_colors.cycle())
		#time.sleep(.1)
		# strip.set_all_pixels()
		# strip.show()

		#i = i + 0.3
		#rainbow(i)
		
		# for x in range(10,63,1):
		# 	strip.set_pixel(x, strip.led_colors.get("White"))	
		#for x in range(64,299,3):
		#	strip.set_pixel(x, strip.led_colors.get("White"))
		#snakes(randint(1,300),0, 255,strip.led_colors.random())
		#strip.show();
		random_snakes()

	
		
except KeyboardInterrupt:
	strip.off()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)
