import sys
import os
import pygame
from pygame.locals import *
import config as cfg
from components.camera import Camera
from components.servo_control import ServoControl


class App(object):
    def __init__(self):
        mode_flags = pygame.DOUBLEBUF
        if cfg.FULLSCREEN:
            mode_flags |= pygame.FULLSCREEN
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption(cfg.DEFAULT_CAPTION)
        self.screen = pygame.display.set_mode(
            (cfg.WIDTH, cfg.HEIGHT), mode_flags)

        self.screen_rect = self.screen.get_rect()
        self.components = {}
        self.clock = pygame.time.Clock()
        self.fps = cfg.FRAMERATE
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.show_fps = False
        self.background_color = (0, 0, 0)

    def add_component(self, name, component):
        self.components[name] = component

    def remove_component(self, name):
        self.components[name].terminate()
        del self.components[name]

    def event_loop(self):
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                self.done = True
            elif event.type == KEYDOWN:
                if event.key == K_F3:
                    self.show_fps = not self.show_fps
                elif event.key == K_ESCAPE:
                    self.done = True
            filtered_events.append(event)

    def update(self, dt):
        """
        Update must acccept and pass dt to all elements that need to update.
        """
        for cp in self.components.values():
            cp.update(dt)
        pass

    def render(self):
        """
        Render all needed elements and update the display.
        """
        self.screen.fill(self.background_color)
        for cp in self.components.values():
            cp.render(self.screen)
        pygame.display.flip()

    def main_loop(self):
        """
        We now use the return value of the call to self.clock.tick to
        get the time delta between frames.
        """
        dt = 0
        self.clock.tick(self.fps)
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(self.fps)/1000.0


def main():
    app = App()
    app.add_component('camera', Camera(
        app.screen.get_size(), camera_index=cfg.CAMERA_INDEX))
    app.add_component('servo', ServoControl())
    app.remove_component('camera')
    app.main_loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
