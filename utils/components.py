import abc
import pygame
from .primitives import Wireframe
from uuid import uuid4


class BaseComponent(metaclass=abc.ABCMeta):
    def __init__(self, position):
        self.childrens = {}
        self.x = position[0]
        self.y = position[1]
        self.parent = None

    def get_global_x(self):
        if self.parent is None:
            return self.x
        else:
            return self.x + self.parent.get_global_x()

    def get_global_y(self):
        if self.parent is None:
            return self.y
        else:
            return self.y + self.parent.get_global_y()

    def get_global_position(self):
        return (self.get_global_x(), self.get_global_y())

    def add_child(self, child, name=None):
        child.parent = self
        if name is None:
            name = uuid4()
        self.childrens[name] = child

    def update_childrens(self, dt: float):
        for child in self.childrens.values():
            child.update(dt)

    def render_childrens(self, render: pygame.Surface):
        for child in self.childrens.values():
            child.render(render)

    @abc.abstractmethod
    def update(self, dt: float):
        print("["+self.__class__.__name__+"] - Override this process event")

    @abc.abstractmethod
    def render(self, render: pygame.Surface):
        print("["+self.__class__.__name__+"] - Override this process event")

    def terminate(self):
        pass


class InputComponent(BaseComponent):
    def process_input_childrens(self, events, keys):
        for child in self.childrens.values():
            child.process_input(events, keys)

    @abc.abstractmethod
    def process_input(self, events, keys):
        print("["+self.__class__.__name__+"] - Override this process event")
        return


class WireFrameComponent(BaseComponent):
    def __init__(self, position, wireframe: Wireframe):
        super().__init__(position)
        self.wireframe = wireframe
        self.show_edges = True
        self.show_nodes = True
        self.node_radius = 4
        self.line_radius = 1
        self.nodes_color = (255, 255, 255)
        self.edges_color = (200, 200, 200)
        self.moved = (0, 0, 0)

    def rotate(self, *args, **kwargs):
        self.wireframe.rotate(*args, **kwargs)

    def scale(self, *args, **kwargs):
        self.wireframe.scale(*args, **kwargs)

    def translate(self, *args, **kwargs):
        self.wireframe.translate(*args, **kwargs)

    def move(self, x, y=0, z=0):
        self.moved = (self.moved[0]+x, self.moved[1]+y, self.moved[2]+z)

    def get_reverse_move(self):
        return (-self.moved[0], -self.moved[1], -self.moved[2])

    def render(self, render: pygame.Surface):
        self.wireframe.translate(self.moved)
        if self.show_edges:
            for n1, n2 in self.wireframe.edges:
                startpos = self.wireframe.nodes[n1][:2] + \
                    [self.get_global_x(), self.get_global_y()]
                endpos = self.wireframe.nodes[n2][:2] + \
                    [self.get_global_x(), self.get_global_y()]
                pygame.draw.aaline(
                    render, self.edges_color, startpos, endpos, self.line_radius)
            if self.show_nodes:
                for node in self.wireframe.nodes:
                    pygame.draw.circle(render, self.nodes_color, (int(
                        node[0]) + self.get_global_x(), int(node[1]) + self.get_global_y()), self.node_radius, 0)
        for child in self.childrens:
            self.render(render)
        self.wireframe.translate(self.get_reverse_move())

    def update(self, dt):
        pass
