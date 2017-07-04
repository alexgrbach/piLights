import time
from random import randint
import edisonBulbs

print("Random Toggle One or whatever...")
try:
	edisonBulbs.setup()
	edisonBulbs.toggle_random_bulbs()
	while True:
		time.sleep(1)
		edisonBulbs.toggle_bulb(edisonBulbs.chan_list[randint(0,7)])
except KeyboardInterrupt:
	print("""
kthxbai!""")
	exit(0)