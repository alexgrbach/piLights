import time
from random import randint
import pistrip as strip
import os as sys

def fire(width = 10, delay=0, r=255, g=255, b=255):
	for x in range(-width, strip.length(),1):
		for y in range(width):
			strip.set_pixel(x+y, r, g, b)
		strip.show()
		time.sleep(delay)
		strip.clear()
	for x in range(strip.length(), -width, -1):
		for y in range(width):
			strip.set_pixel(x+y, r, g, b)
		strip.show()
		time.sleep(delay)
		strip.clear()

def breathe(durriation=5,color=Color(255,255,255)):
	strip.set_all_pixels(color)
	for y in range(60,255, durriation):
			strip.brightness(y)
			strip.show()
	for y in range(255, 60, -durriation):
		strip.brightness(y)
		strip.show()
	strip.clear()

def flash_all(durriation=1, r=255, g=255, b=255):
	strip.set_all_pixels(r,g,b)
	strip.show()
	time.sleep(durriation)
	strip.clear()

def random_int_for_color():
	return randint(0, 255)/randint(1,10)

def random_color():
	return Color(random_int_for_color(), random_int_for_color(), random_int_for_color())

print("""Testing.

""")

try:
	while True:
		#fire(150,0,random_int_for_color(),random_int_for_color(),random_int_for_color())
		#for x in range(randint(1,100)):
		r=random_int_for_color()
		g=random_int_for_color()
		b=random_int_for_color()
		breathe(3,random_color())
		# r=random_int_for_color()
		# g=random_int_for_color()
		# b=random_int_for_color()
		# fire(150,0,r,g,b)
except KeyboardInterrupt:
	strip.off()
	exit(0)