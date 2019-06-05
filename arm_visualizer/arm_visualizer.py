import pygame as pg
from pygame.locals import *
from utils.components import BaseComponent, WireFrameComponent
from utils.primitives import Plane, Cube
from utils.projection_viewer import ProjectionViewer
from gpiozero import AngularServo


class ArmVisualizer(BaseComponent):
    def __init__(self, position=(0,0), size=(100, 100), background_color=(35, 41, 53)):
        super().__init__(position=position)
        self.projection = ProjectionViewer(size, background=background_color, center=True)
        # Lets use 4 pins: 17, 18, 22 and 23
        self.base = WireFrameComponent((0,0), Plane(100, 100))
        self.projection.add_wireframe("base", self.base)

        self.motor_base = WireFrameComponent((0,0), Cube(20, 40, 40))
        self.motor_base.move(20, 0)
        self.projection.add_wireframe("motor_base", self.motor_base)
    

    def update(self, dt: float):
        self.motor_base.rotate((dt, dt, dt))
        self.base.rotate((dt, dt, dt))
        self.update_childrens(dt)
    

    def render(self, render: pg.Surface):
        render.blit(self.projection.render(), self.get_global_position())
