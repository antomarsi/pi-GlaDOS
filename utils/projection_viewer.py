import pygame
from pygame.locals import *
from .components import WireFrameComponent, BaseComponent
from typing import Dict


class ProjectionViewer(object):
    def __init__(self, width_height, height=None, background=(26, 37, 48), center=True):
        if height is None:
            self.width = width_height[0]
            self.height = width_height[1]
        else:
            self.width = width_height
            self.height = height
        self.surface = pygame.Surface(
            (self.width, self.height), flags=SRCALPHA)
        self.background = background
        self.wireframes: Dict[str, WireFrameComponent] = {}
        if center:
            self.render_pivot = (self.width/2, self.height/2)

    def moveAll(self, x, y):
        for wireframe in self.wireframes.values():
            wireframe.move(x, y)

    def get_wireframe(self, name):
        return self.wireframes[name]

    def add_wireframe(self, name, wireframe: WireFrameComponent):
        self.wireframes[name] = wireframe

    def remove_wireframe(self, name):
        del self.wireframes[name]

    def render(self):
        self.surface.fill(self.background)
        for wireframe in self.wireframes.values():
            wireframe.render(self.surface)
        return self.surface
