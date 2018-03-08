import time
import sys

now = int(time.time())
future = now + 1 
while time.time() < future:
    # do stuff
    future = future +1
    print(future)
    if sys.stdin.read(1) == 'l':
    	pass