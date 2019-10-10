
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import AngularServo, Device
import logging


class ServoController(BaseComponent):
    def __init__(self, socket, pin, debug=True):
        super().__init__(socket)
        self.pin = pin
        if debug:
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    def process(self):
        logging.info("Processing ServoController")
        logging.info("Current Angle: {}".format(self.servo.angle))

    def start(self):
        myCorrection = 0
        maxPW = (2.0 + myCorrection) / 1000
        minPW = (1.0 - myCorrection) / 1000
        self.servo = AngularServo(
            self.servopin, 0, min_pulse_width=minPW, max_pulse_width=maxPW)
        self.servo.mid()
        super().start()
