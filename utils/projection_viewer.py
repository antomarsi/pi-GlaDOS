import pygame
from pygame.locals import *
from .components import WireFrameComponent, BaseComponent
from typing import Dict


class ProjectionViewer(object):
    def __init__(self, width_height, height=None, background=(26, 37, 48), center=True, outline=None):
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
        self.center = center
        self.outline = outline

    def moveAll(self, x, y):
        for wireframe in self.wireframes.values():
            wireframe.move(x, y)

    def get_wireframe(self, name):
        return self.wireframes[name]

    def add_wireframe(self, wireframe: WireFrameComponent, name):
        if self.center:
            wireframe.x = int(self.width/2)
            wireframe.y = int(self.height/2)
        self.wireframes[name] = wireframe

    def remove_wireframe(self, name):
        del self.wireframes[name]

    def render(self):
        self.surface.fill(self.background)
        if self.outline is not None:
            pygame.draw.lines(self.surface, self.outline, True, [
                (0, 0), (0, self.height-1),
                (self.width-1, self.height-1), (self.width-1, 0)], 3)
        for wireframe in self.wireframes.values():
            wireframe.render(self.surface)
        return self.surface
