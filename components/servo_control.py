import config
from utils.components import BaseComponent
from utils.primitives import Vector2, Cube, Sphere
from utils.projection_viewer import ProjectionViewer
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device
import pygame
from pygame.locals import *
import os


class ServoControl(BaseComponent):
    def __init__(self, size=(200, 100), gpio1=18, gpio2=17, angles=(-42, 44)):
        self.surface = pygame.Surface(size, flags=SRCALPHA)
        self.font = pygame.font.SysFont(None, 16)
        self.projview = ProjectionViewer(200, 200)
        cube = Cube(20, 20, 20)
        cube.move(20, 20)
        cube.scale((2, 2, 1))
        shpere = Sphere(20, 20)
        shpere.move(60, 60)

        cylinder = Cylinder(20, 20)
        cylinder.move(80, 60)


        self.projview.add_wireframe('cube', cube)
        self.projview.add_wireframe('shpere', shpere)
        self.projview.add_wireframe('cylinder', cylinder)
        self.color = (255, 0, 0)
        ### INIT SERVOS ###
        if config.MOCK_GPIO:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)
        self.servo_y = AngularServo(
            gpio1, min_angle=angles[0], max_angle=angles[1])
        self.servo_x = AngularServo(
            gpio2, min_angle=angles[0], max_angle=angles[1])

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
        self.projview.get_wireframe('shpere').rotate((dt, dt, dt))
        self.projview.get_wireframe('cube').rotate((dt, dt, dt))
        self.projview.get_wireframe('cylinder').rotate((dt, dt, dt))
        pass

    def render(self, render: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        # Circle X
        vecX = Vector2(25, 25)
        vecX.rotate(self.servo_x.value)
        pygame.draw.circle(self.surface, (0, 254, 255), (25, 25), 25, 1)
        text_surf = self.font.render(
            "X: %.3f" % (self.servo_x.value), True, (0, 254, 255))
        self.surface.blit(text_surf, (0, 50))

        # Circle Y
        pygame.draw.circle(self.surface, (232, 127, 0), (80, 25), 25, 1)
        text_surf = self.font.render(
            "Y: %.3f" % (self.servo_y.value), True, (232, 127, 0))
        self.surface.blit(text_surf, (55, 50))
        render.blit(self.surface, (10, 10))
        render.blit(self.projview.render(), (200, 200))
