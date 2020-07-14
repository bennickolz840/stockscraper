import time 
from datetime import datetime
from analysis import analyzer 

infinite = True
while infinite:
    now = datetime.now()
    cutOff = now.replace(hour=19, minute=0, second=0, microsecond=0)
    startTime = now.replace(hour=8, minute=30, second=0, microsecond=0)
    while startTime <= now <= cutOff:
        print("Inside Loop")
        analyzer()
        time.sleep(120)
