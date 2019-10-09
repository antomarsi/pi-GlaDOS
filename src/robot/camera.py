import time
import numpy as np
from multiprocessing import Process, Queue 

class Camera:
    def __init__(self, queue, index, camera_size=(320,240), verbose="False", debug=True):
        self.q = queue
        self.camera_index = index
        self.verbose = verbose
        self.size = camera_size

    def start(self):
        self.p = Process(target=self.run, args=((self.q),))
        self.p.start()

    def process_opencv(self):
        ret, frame = self.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.frame = frame

    def run(self, queue):
        self.camera = cv2.VideoCapture(self.camera_index)
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
        self.camera.set(3, self.size[0])
        self.camera.set(4, self.size[1])
        self.servo = AngularServo(self.pin, 0, min_pulse_width=minPW, max_pulse_width=maxPW)
        self.faces = []
        self.frame = None

        while True:
                self.process_opencv()
            try:
                inp = queue.get_nowait()
                if inp[0] == "command":
                    axis = inp[1]
                    if self.verbose:
                        print("[Servo] Dutycycle changed to {}, {}".format(axis, self.x))
            except:
                time.sleep(0.001)
                pass

if __name__ == "__main__":
    pass

