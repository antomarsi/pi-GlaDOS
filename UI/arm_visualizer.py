import pygame as pg
from pygame.locals import *
from utils.components import BaseComponent, WireFrameComponent
from utils.primitives import Plane, Cube, Line
from utils.projection_viewer import ProjectionViewer
from utils.colors import COLORS, hex_to_rgb
from arm.servo_control import ServoControl

class ArmVisualizer(BaseComponent):
    def __init__(self, position=(0,0), size=(100, 100), background_color=COLORS[1]):
        super().__init__(position=position)
        self.font = pg.font.SysFont("monospace", 15)

        self.projection = ProjectionViewer(size, background=background_color, outline=COLORS[3])
        # Lets use 4 pins: 17, 18, 22 and 23
        self.servo_control = ServoControl()
        self.control_angle = self.servo_control.get_angle()

        self.motor_base = WireFrameComponent((0,0), Cube(20, 20, 20), edge_color=COLORS[5])
        self.line_base_body = WireFrameComponent((0,0), Line(50), edge_color=hex_to_rgb("#FF00FF"))

        self.motor_body = WireFrameComponent((0, 0), Cube(20, 20, 20), edge_color=COLORS[5])
        self.motor_body.translate((50, 0, 0))

        self.line_body_head = WireFrameComponent((0,0), Line(50), edge_color=hex_to_rgb("#00FFFF"))
        self.line_body_head.translate((50, 0, 0))
        
        self.motor_head = WireFrameComponent((0, 0), Cube(20, 20, 20), edge_color=COLORS[5])
        self.motor_head.translate((100, 0, 0))

        self.motor_base.set_local_translation(-100, 0, 0)
        self.motor_base.set_local_rotation(45, 0, 90)

        self.motor_base.show_axis = True
        self.motor_body.show_axis = True
        self.motor_head.show_axis = True

        self.motor_base.add_child(self.line_base_body, "line_base_body")
        self.line_base_body.add_child(self.motor_body, "motor_body")
        self.motor_body.add_child(self.line_body_head, "line_body_head")
        self.line_body_head.add_child(self.motor_head, "motor_head")

        self.projection.add_wireframe(self.motor_base, "motor_base")

    def update(self, dt: float):
        self.control_angle = self.servo_control.get_angle()
        self.update_childrens(dt)
    

    def render(self, render: pg.Surface):
        render.blit(self.projection.render(), self.get_global_position())

        label = self.font.render("X: {} Y: {}".format(self.control_angle[0], self.control_angle[1]), 1, COLORS[7])
        render.blit(label, self.get_global_position())