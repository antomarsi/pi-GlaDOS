import config
from utils.primitives import Vector2, Cube, Plane, Sphere
from utils.projection_viewer import ProjectionViewer
from utils.components import BaseComponent
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device
import pygame
from pygame.locals import *
import os
from UI.arm_visualizer import ArmVisualizer


class ServoVizualiser(BaseComponent):
    def __init__(self, size=(400, 100), position=(0, 0)):
        super().__init__(position)
        self.surface = pygame.Surface(size, flags=SRCALPHA)
        self.font = pygame.font.SysFont(None, 28)
        self.projview = ProjectionViewer(size)
        self.color = (255, 0, 0)
        ### INIT SERVOS ###
        gpio1 = 18
        gpio2 = 17
        angles = (-42, 44)
        if config.MOCK_GPIO:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)
        self.servo_y = AngularServo(
            gpio1, min_angle=angles[0], max_angle=angles[1])
        self.servo_x = AngularServo(
            gpio2, min_angle=angles[0], max_angle=angles[1])

        self.add_child(name="visualizer", child=ArmVisualizer(
            position=(5, 5), size=(size[0]-10, (size[1]/2))))

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
        self.update_childrens(dt)
        pass

    def render(self, render: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.projview.render(), (0, 0))
        render.blit(self.surface, self.get_global_position())
        self.render_childrens(render)
