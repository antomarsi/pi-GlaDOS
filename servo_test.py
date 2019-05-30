from gpiozero import Servo
from time import sleep
from easing_functions import *
import numpy as np

myGPIO = 17

myCorrection = 0.45

maxPW = (2.0 + myCorrection)/1000
minPW = (1.0 - myCorrection)/1000

servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
a = QuadEaseInOut(start=-1, end = 1, duration = 5)
x = np.arange(0, 5, 0.5)
y0 = list(map(a.ease, x))
for y in y0:
    print(y)
    sleep(0.5)