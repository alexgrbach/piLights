import time
import pistrip as strip
import os as sys

from random import randint
from neopixel import *

def fire_cycle(width = 10, delay=0, brightness=128, color=strip.led_colors.get("White")):
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

def cycle_all_colors():
	color = strip.led_colors.cycle()
	#exclude black
	if(color == 0):
		color = strip.led_colors.cycle()
	return (color)



print("Testing...")

try:
	while True:
		#breathe(3, 60, 255, strip.random_color())
		flash_all(10, cycle_all_colors())
		# fire(randint(1,300),0, 255,strip.led_colors.random())
		#fire_down(1,0,255,cycle_all_colors())

		#print(strip.led_colors.cycle())
		#time.sleep(.1)
except KeyboardInterrupt:
	strip.off()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)