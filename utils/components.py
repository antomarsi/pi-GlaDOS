import abc
import pygame
from .primitives import Wireframe, Line
from uuid import uuid4
from .colors import COLORS

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
    def __init__(self, position, wireframe: Wireframe, node_color=COLORS[7], edge_color=COLORS[6]):
        super().__init__(position)
        self.wireframe = wireframe
        self.show_edges = True
        self.show_nodes = True
        self.node_radius = 4
        self.line_radius = 1
        self.nodes_color = node_color
        self.edges_color = edge_color
        self.local_translation = (0, 0, 0)
        self.local_rotation = (0, 0, 0)
        self.local_scale = (0, 0, 0)
        self.show_axis = False
        alix_width = 25
        self.axis_line = (
            Line(alix_width, 0, 0),
            Line(0, -alix_width, 0),
            Line(0, 0, alix_width)
            )
        self.local_line = (self.axis_line[0].nodes, self.axis_line[1].nodes, self.axis_line[2].nodes)
        self.local_nodes = self.wireframe.nodes
        

    def rotate(self, *args, **kwargs):
        self.wireframe.rotate(*args, **kwargs)
        self.axis_line[0].rotate(*args, **kwargs)
        self.axis_line[1].rotate(*args, **kwargs)
        self.axis_line[2].rotate(*args, **kwargs)

    def scale(self, *args, **kwargs):
        self.wireframe.scale(*args, **kwargs)
        self.axis_line[0].scale(*args, **kwargs)
        self.axis_line[1].scale(*args, **kwargs)
        self.axis_line[2].scale(*args, **kwargs)
        

    def translate(self, *args, **kwargs):
        self.wireframe.translate(*args, **kwargs)
        self.axis_line[0].translate(*args, **kwargs)
        self.axis_line[1].translate(*args, **kwargs)
        self.axis_line[2].translate(*args, **kwargs)

    def local_move(self, x, y=0, z=0):
        self.local_translation = (self.local_translation[0]+x, self.local_translation[1]+y, self.local_translation[2]+z)

    def local_rotate(self, x, y=0, z=0):
        self.local_rotation = (self.local_rotation[0]+x, self.local_rotation[1]+y, self.local_rotation[2]+z)

    def set_local_rotation(self, x, y=0, z=0):
        self.local_rotation = (x, y, z)

    def set_local_translation(self, x, y=0, z=0):
        self.local_translation = (x, y, z)

    def reset_rotation(self):
        self.local_rotation = (0, 0, 0)

    def reset_translation(self):
        self.local_translation = (0, 0, 0)

    def get_local_translation(self):
        value = self.local_translation
        if self.parent != None and type(self.parent) is type(self):
            pvalue = self.parent.get_local_translation()
            value = (value[0] + pvalue[0], value[1] + pvalue[1], value[2] + pvalue[2])
        return value

    def get_local_rotation(self):
        value = self.local_rotation
        if self.parent != None and type(self.parent) is type(self):
            pvalue = self.parent.get_local_rotation()
            value = (value[0] + pvalue[0], value[1] + pvalue[1], value[2] + pvalue[2])
        return value

    def process_local(self):
        lt = self.get_local_translation()
        lr = self.get_local_rotation()
        self.local_line = (self.axis_line[0].nodes, self.axis_line[1].nodes, self.axis_line[2].nodes)
        self.local_nodes = self.wireframe.nodes
        self.translate(lt)
        self.rotate(lr)

    def reverse_local(self):
        self.wireframe.nodes = self.local_nodes
        self.axis_line[0].nodes = self.local_line[0]
        self.axis_line[1].nodes = self.local_line[1]
        self.axis_line[2].nodes = self.local_line[2]
        self.local_nodes = self.wireframe.nodes


    def render(self, render: pygame.Surface):
        self.process_local()
        if self.show_edges:
            for n1, n2 in self.wireframe.edges:
                startpos = self.wireframe.nodes[n1][:2] + \
                    [self.get_global_x(), self.get_global_y()]
                endpos = self.wireframe.nodes[n2][:2] + \
                    [self.get_global_x(), self.get_global_y()]
                pygame.draw.line(
                    render, self.edges_color, startpos, endpos, self.line_radius)
            if self.show_nodes:
                for node in self.wireframe.nodes:
                    pygame.draw.circle(render, self.nodes_color, (int(
                        node[0]) + self.get_global_x(), int(node[1]) + self.get_global_y()), self.node_radius, 0)
            if self.show_axis == True:
                axiscolors = ((255,0,0), (0,255,0), (0,0,255))
                for idx, val, in enumerate(self.axis_line):
                    for n1, n2 in val.edges:
                        startpos = val.nodes[n1][:2] + [self.get_global_x(), self.get_global_y()]
                        endpos = val.nodes[n2][:2] + [self.get_global_x(), self.get_global_y()]
                        pygame.draw.line(render, axiscolors[idx], startpos, endpos, 1)
                    node = val.nodes[1]
                    pygame.draw.circle(render, axiscolors[idx], (int(node[0]) + self.get_global_x(), int(node[1]) + self.get_global_y()), self.node_radius, 0)
        for child in self.childrens.values():
            child.render(render)
        self.reverse_local()

    def update(self, dt):
        pass
