import pygame as pg
from pygame.locals import *
import time
import math
import cv2
import numpy as np
import os
from utils.components import BaseComponent
from .facetracker import FaceTracker


class Camera(BaseComponent):
    def __init__(self, size, color=(0, 255, 0), camera_index=0):
        self.cascade = cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
        self.camera = cv2.VideoCapture(camera_index)
        self.camera.set(3, size[0])
        self.camera.set(4, size[1])
        self.color = color
        self.surface = None
        self.face_tracker = FaceTracker(self.cascade)
        self.faces = []
        self.deadzone_color = (255, 0, 255)
        self.landmarks = None
        self.deadzone_radius = size[0]/8

    def update(self, dt):
        ret, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.faces = self.face_tracker.detect(frame)
        frame = np.rot90(frame)
        frame = cv2.flip(frame, 0)
        self.surface = pg.surfarray.make_surface(frame)

    def check_if_face_deadzone(self):
        if self.face is None:
            return False
        return self.deadzone_rect.collidepoint(self.face.center)

    def draw_face(self):
        for face in self.faces:
            pg.draw.rect(self.surface, (0, 172, 0), face, 2)
            color = ((255, 0, 0) if self.get_distance(face)
                     >= self.deadzone_radius else (0, 255, 0))
            pg.draw.line(self.surface, color,
                         face.center, self.surface.get_rect().center, 1)

    def get_distance(self, face):
        rect = self.surface.get_rect()
        distance = math.hypot(face.centerx-rect.centerx,
                              face.centery-rect.centery)
        return distance

    def draw_deadzone(self):
        pg.draw.circle(self.surface, self.deadzone_color, self.surface.get_rect().center,
                       int(self.deadzone_radius), 1)

    def render(self, render):
        if self.surface is None:
            return
        self.draw_deadzone()
        self.draw_face()
        render.blit(self.surface, (0, 0))
