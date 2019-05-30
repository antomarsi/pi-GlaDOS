
"""
Created on Fri Nov 9

@author: Anjith George,
email: anjith2006@gmail.com

For details refer to:

1. Dasgupta A, George A, Happy SL, Routray A. A vision-based system for monitoring the loss of attention in automotive drivers. IEEE Transactions on Intelligent Transportation Systems. 2013 Dec;14(4):1825-38.
2. George A, Dasgupta A, Routray A. A framework for fast face and eye detection. arXiv preprint arXiv:1505.03344. 2015 May 13.
"""


import numpy as np
import cv2
import pygame as pg


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
