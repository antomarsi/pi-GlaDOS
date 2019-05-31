import pygame
from pygame.locals import *
from .primitives import Wireframe


class ProjectionViewer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface(
            (self.width, self.height), flags=SRCALPHA)
        self.wireframes = {}

    def get_wireframe(self, name):
        return self.wireframes[name]

    def add_wireframe(self, name, wireframe: Wireframe):
        self.wireframes[name] = wireframe

    def remove_wireframe(self, name):
        del self.wireframes[name]

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        for wireframe in self.wireframes.values():
            if wireframe.show_edges:
                for n1, n2 in wireframe.edges:
                    startpos = wireframe.nodes[n1][:2] + \
                        [wireframe.x, wireframe.y]
                    endpos = wireframe.nodes[n2][:2] + \
                        [wireframe.x, wireframe.y]
                    pygame.draw.aaline(
                        self.surface, wireframe.edges_color, startpos, endpos, wireframe.line_radius)
            if wireframe.show_nodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.surface, wireframe.nodes_color, (int(
                        node[0]) + wireframe.x, int(node[1]) + wireframe.y), wireframe.node_radius, 0)
        return self.surface
