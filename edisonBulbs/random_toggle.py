import time
import edisonBulbs

##Program starts here	
print("Running...")
try:
	edisonBulbs.setup()
	while True:
		edisonBulbs.toggle_random_bulbs()
		time.sleep(300)
except KeyboardInterrupt:
	print("""
kthxbai!""")
	exit(0)