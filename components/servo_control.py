import config
from utils.components import BaseComponent, WireFrameComponent
from utils.primitives import Vector2, Cube, Plane, Sphere
from utils.projection_viewer import ProjectionViewer
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device
import pygame
from pygame.locals import *
import os


class ServoControl(BaseComponent):
    def __init__(self, size=(400, 100), gpio1=18, gpio2=17, angles=(-42, 44), position=(0, 0)):
        super().__init__(position)
        self.surface = pygame.Surface(size, flags=SRCALPHA)
        self.font = pygame.font.SysFont(None, 28)
        self.projview = ProjectionViewer(size)
        self.color = (255, 0, 0)
        ### INIT SERVOS ###
        if config.MOCK_GPIO:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)
        self.servo_y = AngularServo(
            gpio1, min_angle=angles[0], max_angle=angles[1])
        self.servo_x = AngularServo(
            gpio2, min_angle=angles[0], max_angle=angles[1])
        self.create_wireframe_model()

    def create_wireframe_model(self):
        base = WireFrameComponent((0, 0), Sphere(50))
        self.projview.add_wireframe('base', base)
        self.projview.get_wireframe('base').move(60,60)

    def clamped_servo_x(self, value: float):
        return max(self.servo_x.min_angle, min(value, self.servo_x.max_angle))

    def clamped_servo_y(self, value: float):
        return max(self.servo_y.min_angle, min(value, self.servo_y.max_angle))

    def reset(self):
        self.servo_x.value = 0
        self.servo_y.value = 0
        pass

    def angle_two_points(self, p1: Vector2, p2: Vector2):
        # return Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / Math.PI
        pass

    def move(self, x: float, y: float):
        self.servo_x.value = self.clamped_servo_x(x)
        self.servo_y.value = self.clamped_servo_y(y)
        pass

    def update(self, dt: float):
        self.projview.get_wireframe("base").rotate((dt, dt, dt))
        pass

    def render(self, render: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.projview.render(), (0, 0))
        render.blit(self.surface, (self.x, self.y))
