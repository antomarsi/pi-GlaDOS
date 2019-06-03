import cv2
import pygame as pg


class FaceTracker():
    def __init__(self, cascade_fn, scale=1, scaleFactor=1.3, minSize=(30, 30), skip_frames=2):
        self.frames = 0
        self.cascade = cv2.CascadeClassifier(cascade_fn)
        self.scale = scale
        self.scaleFactor = scaleFactor
        self.minSize = minSize
        self.prev_points = []
        self.faces = []
        self.skip_frames = skip_frames
        self.current_frames = self.skip_frames

    def detect(self, frame):
        if self.current_frames >= self.skip_frames:
            self.current_frames = 0
            self.faces = []
            faces = self.cascade.detectMultiScale(
                frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for face in faces:
                (x, y, w, h) = face
                self.faces.append(pg.Rect(x, y, w, h))
        self.current_frames += 1
        return self.faces
