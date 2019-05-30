import pygame
from pygame.locals import *
import time
import cv2
import numpy as np
import os
from gtts import gTTS
from io import BytesIO
from time import sleep


# Face
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
SCREEN = [640, 360]
camera = cv2.VideoCapture(0)
camera.set(3, SCREEN[0])
camera.set(4, SCREEN[1])
GREEN = (0, 255, 0)

pygame.mixer.init()

texts = [
    "Initializing GlaDOS",
    "Loading",
    "Hello, are you there?",
    "Oh, i see you"
]
voices = []

for text in texts:
    sound_file = BytesIO()
    tts = gTTS(text, 'en')
    tts.write_to_fp(sound_file)
    sound_file.seek(0)
    voices.append(sound_file)

def play_sound(index):
    pygame.mixer.music.load(voices[index])
    pygame.mixer.music.play()

def get_faces(image):
    return faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )


if __name__ == '__main__':
    pygame.init()  # Initialize pygame
    screen = pygame.display.set_mode(SCREEN)

    running = True
    play_sound(0)
    face_detected = False
    while running:  # Ze loop

        ret, frame = camera.read()

        time.sleep(1 / 120)  # 60 frames per second
        print(pygame.mixer.music.get_busy())
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = get_faces(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        frame = np.rot90(frame)
        frame = cv2.flip(frame, 0)

        frame = pygame.surfarray.make_surface(frame)
        screen.fill([0, 0, 0])
        screen.blit(frame, (0, 0))
        if len(faces) > 0 and not face_detected:
            face_detected = True
            play_sound(3)
            
        for (x, y, w, h) in faces:
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(screen, GREEN, rect,  2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
    pygame.quit()
