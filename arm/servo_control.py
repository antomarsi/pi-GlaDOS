import config
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device
from utils.primitives import Vector2
import pygame
from pygame.locals import *
import os

class ServoControl():
    def __init__(self, base_gpio=18, head_gpio=17):
        myCorrection=0
        maxPW=(2.0+myCorrection)/1000
        minPW=(1.0-myCorrection)/1000

        if config.MOCK_GPIO:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)
        self.servo_base = AngularServo(base_gpio, 0, min_pulse_width=minPW, max_pulse_width=maxPW)
        self.servo_head = AngularServo(head_gpio, 0, min_pulse_width=minPW, max_pulse_width=maxPW)


    def clamped_servo_base(self, value: float):
        return max(self.servo_base.min_angle, min(value, self.servo_base.max_angle))

    def clamped_servo_head(self, value: float):
        return max(self.servo_head.min_angle, min(value, self.servo_head.max_angle))

    def reset(self):
        self.servo_base.mid()
        self.servo_head.mid()
        pass
    
    def get_angle(self):
        return (self.servo_base.angle, self.servo_head.angle)

    def angle_two_points(self, p1: Vector2, p2: Vector2):
        # return Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / Math.PI
        pass

    def move(self, x: float, y: float):
        self.servo_base.angle = self.clamped_servo_base(x)
        self.servo_head.angle = self.clamped_servo_head(y)
        pass

    def update(self):
        pass