import pygame as pg
from pygame.locals import *
import time
import math
import cv2
import numpy as np
import os
from utils.components import BaseComponent


class FaceTracker():
    def __init__(self, cascade_fn, scale=1, scaleFactor=1.3, minSize=(30, 30)):
        self.prev_angle = 0
        self.frames = 0
        self.cascade = cv2.CascadeClassifier(cascade_fn)
        self.scale = scale
        self.scaleFactor = scaleFactor
        self.minSize = minSize
        self.prev_points = []

    def detect(self, frame):
        faces = self.cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            return pg.Rect(x, y, w, h)
        return None


class Camera(BaseComponent):
    def __init__(self, size, color=(0, 255, 0), camera_index=0):
        self.cascade = cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
        self.camera = cv2.VideoCapture(camera_index)
        self.camera.set(3, size[0])
        self.camera.set(4, size[1])
        self.color = color
        self.surface = None
        self.face_tracker = FaceTracker(self.cascade)
        self.face = None
        self.deadzone_color = (255, 0, 255)
        self.landmarks = None
        self.face_timer = 0
        self.face_time = 1
        self.deadzone_radius = size[0]/8

    def update(self, dt):
        ret, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face = self.face_tracker.detect(frame)

        if face is not None:
            self.face = face
            self.face_timer = 0
        elif face is None and self.face_timer >= self.face_time:
            self.face = None
        if self.face is not None:
            self.face_timer += dt
        frame = np.rot90(frame)
        frame = cv2.flip(frame, 0)
        self.surface = pg.surfarray.make_surface(frame)

    def check_if_face_deadzone(self):
        if self.face is None:
            return False
        return self.deadzone_rect.collidepoint(self.face.center)

    def draw_face(self):
        if self.face is not None:
            pg.draw.rect(self.surface, self.color, self.face, 2)

    def get_distance(self):
        rect = self.surface.get_rect()
        distance = math.hypot(self.face.centerx-rect.centerx,
                              self.face.centery-rect.centery)
        print(distance)
        return distance

    def draw_deadzone(self):
        pg.draw.circle(self.surface, self.deadzone_color, self.surface.get_rect().center,
                       int(self.deadzone_radius), 1)
        if self.face is not None:
            color = (0, 0, 255)
            if self.get_distance() > self.deadzone_radius:
                color = (255, 0, 0)
            pg.draw.line(self.surface, color,
                         self.face.center, self.surface.get_rect().center, 1)

    def render(self, render):
        if self.surface is None:
            return
        self.draw_face()
        self.draw_deadzone()
        render.blit(self.surface, (0, 0))
