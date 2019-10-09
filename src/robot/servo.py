#!/usr/bin/python
"""
0.4 Amps/phase
0.11 Nm holding torque
0.9 deg step angle - 400 steps
"""
import time
import numpy as np
from multiprocessing import Process, Queue 
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device

class Servo:
    def __init__(self, queue, pin, verbose="False", debug=True):
        self.q = queue
        self.servopin = pin
        self.verbose = verbose
        if debug:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def clamped_servo(self, value: float):
        return max(self.servo.min_angle, min(value, self.servo.max_angle))

    def run(self, queue):
        inp = (0,0,0)
        myCorrection = 0
        maxPW = (2.0 + myCorrection) / 1000
        minPW = (1.0 - myCorrection) / 1000
        self.servo = AngularServo(self.servopin, 0, min_pulse_width=minPW, max_pulse_width=maxPW)
        self.servo.mid()

        while True:
            try:
                inp = queue.get_nowait()
                if inp[0] == "right":
                    axis = inp[1]
                    self.servo.angle = self.clamped_servo(axis)
                    if self.verbose:
                        print("[Servo] Angle changed to {}, {}".format(axis, self.servo.angle))
            except:
                time.sleep(0.001)
                pass

if __name__ == "__main__":
    myCorrection = 0
    maxPW = (2.0 + myCorrection) / 1000
    minPW = (1.0 - myCorrection) / 1000
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    servo = AngularServo(7, 0, min_pulse_width=minPW, max_pulse_width=maxPW)

    for i in range(10):
        servo.angle = max(servo.min_angle, min(i, servo.max_angle))
        time.sleep(0.5)
        print(servo.angle)

