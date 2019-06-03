import abc
import pygame
from uuid import uuid4


class BaseComponent(metaclass=abc.ABCMeta):
    def __init__(self):
        self.childrens = {}

    def add_child(self, child, name=None):
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
