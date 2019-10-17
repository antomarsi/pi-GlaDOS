import cv2


class FaceTracker():
    def __init__(self, camera_index=0, cascade_fn=cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml", scale=1, scaleFactor=1.3, minSize=(30, 30), skip_frames=2):
        self.camera = cv2.VideoCapture(camera_index)
        self.camera.set(3, size[0])
        self.camera.set(4, size[1])
        self.frames = 0
        self.cascade = cv2.CascadeClassifier(cascade_fn)
        self.scale = scale
        self.scaleFactor = scaleFactor
        self.minSize = minSize
        self.prev_points = []
        self.faces = []
        self.skip_frames = skip_frames
        self.current_frames = self.skip_frames

    def update(self):
        ret, frame = self.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.detect(gray)
        self.frame = self.draw_rect(frame)

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
                self.faces.append((x, y, w, h))
        self.current_frames += 1
        return self.faces

    def draw_rect(self, frame):
        for idx, value in enumerate(self.faces):
            (x, y, w, h) = value
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, 'Face {}'.format(idx), x+(w/2), y+h), font, 1, (200, 255, 155))
        return frame
