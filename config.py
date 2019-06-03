import os

FRAMERATE = int(os.getenv('PI_GLADOS_FRAMERATE', 30))
WIDTH = int(os.getenv('PI_GLADOS_WIDTH', 720))
HEIGHT = int(os.getenv('PI_GLADOS_HEIGHT', 480))
CAMERA_WIDTH = int(os.getenv('PI_GLADOS_CAMERA_WIDTH', 640))
CAMERA_HEIGHT = int(os.getenv('PI_GLADOS_CAMERA_HEIGHT', 480))
FULLSCREEN = int(os.getenv('PI_GLADOS_FULLSCREEN', 0)) == 1
DEFAULT_CAPTION = os.getenv('PI_GLADOS_DEFAULT_CAPTION', "piGladOS v0.1")
CAMERA_INDEX = int(os.getenv('PI_GLADOS_CAMERA_INDEX', 0))

MOCK_GPIO = os.getenv('GPIOZERO_PIN_FACTORY', 'mock') == 'mock'