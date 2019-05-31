import numpy as np
import cv2
import pygame as pg
from gpiozero import AngularServo

class ServoControl():
    def __init__(self, gpio1=18, gpio2=17):
        self.surface = pg.Surface((100, 100))
        self.font = pg.font.SysFont(None, 48)
        self.servo_y = AngularServo(gpio1, min_angle=-42, max_angle=44)
        self.servo_x = AngularServo(gpio1, min_angle=-42, max_angle=44)
    
    def update(self, dt):
        pass

    def render(self, render):
        pass