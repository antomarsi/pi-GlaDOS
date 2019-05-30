import sys, os
import pygame as pg
from pygame.locals import *
import config as cfg
from camera import Camera


class App(object):
    def __init__(self):
        mode_flags = pg.DOUBLEBUF
        if cfg.FULLSCREEN:
            mode_flags |= pg.FULLSCREEN
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        pg.display.set_caption(cfg.DEFAULT_CAPTION)
        self.screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT), mode_flags)

        self.screen_rect = self.screen.get_rect()
        self.camera = Camera(self.screen.get_size())
        self.clock = pg.time.Clock()
        self.fps = cfg.FRAMERATE
        self.done = False
        self.keys = pg.key.get_pressed()
        self.show_fps = False
        self.background_color = (0, 0, 0)

    def event_loop(self):
        pressed_keys = pg.key.get_pressed()
        filtered_events = []
        for event in pg.event.get():
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
        self.camera.update(dt)
        pass

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

    def render(self):
        """
        Render all needed elements and update the display.
        """
        self.screen.fill(self.background_color)
        self.camera.render(self.screen)
        pg.display.flip()


def main():
    app = App()
    app.main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
