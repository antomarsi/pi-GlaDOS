import pygame as pg
from pygame.locals import *
from utils.components import BaseComponent


class ArmVisualizer(BaseComponent):
    def __init__(self, rect=pg.Rect(100, 100, 100, 100), background_color=(52, 62, 80)):
        super().__init__()
        self.rect = rect
        self.surface = pg.Surface((200, 200), flags=SRCALPHA)
        self.background_color = background_color
        self.border = pg.Surface(self.rect.size, flags=SRCALPHA)
        pg.draw.rect(self.border, (254, 158, 12), pg.Rect(
            3, 3, self.rect.width-6, self.rect.height-6), 2)

    def update(self, dt: float):
        self.update_childrens(dt)

    def render(self, render: pg.Surface):
        self.surface.fill(self.background_color)
        self.render_childrens(self.surface)
        scaled = pg.transform.scale(
            self.surface, (self.rect.width, self.rect.height))
        scaled.blit(self.border, (0, 0))
        render.blit(scaled, (self.rect.x, self.rect.y))
