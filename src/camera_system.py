import cv2
import logging
from utils import BaseComponent

class CameraSystem(BaseComponent):
    def __init__(self, sockets, index=0, camera_size=(320,240), debug=True):
        super().__init__(sockets)
        self.camera_index = index
        self.size = camera_size
        self.faces = []

    def process(self):
        logging.info("Processing CameraSystem")
        ret, frame = self.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in self.faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.frame = frame
        logging.info("{} faces detected".format(len(self.faces)))

    def start(self):
        self.camera = cv2.VideoCapture(self.camera_index)
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
        self.camera.set(3, self.size[0])
        self.camera.set(4, self.size[1])
        self.faces = []
        self.frame = None
        super().start()
