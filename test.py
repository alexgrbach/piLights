import time
from random import randint
import pistrip as strip

def fire(width = 10, delay=0, r=255, g=255, b=255):
	for x in range(strip.length()):
		for y in range(width):
			strip.set_pixel(x+y, r, g, b)
		strip.show()
		time.sleep(delay)
		strip.clear()
	for x in range(strip.length(), -1, -1):
		for y in range(width):
			strip.set_pixel(x+y, r, g, b)
		strip.show()
		time.sleep(delay)
		strip.clear()

print("""Testing.

""")

while True:
	r = randint(0, 255)/randint(1,10)
	g = randint(0,255)/randint(1,10)
	b = randint(0,255)/randint(1,10)
	fire(200,0,r,g,b)

strip.off()      