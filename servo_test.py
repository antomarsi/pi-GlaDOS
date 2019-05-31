from gpiozero import Servo, AngularServo
from time import sleep

myGPIO = 18

myCorrection = 0.60
maxPW = (2.0+myCorrection)/1000
minPW = (1.0-myCorrection)/1000

servo = Servo(17, min_pulse_width=minPW, max_pulse_width=maxPW)
servo2 = Servo(18, min_pulse_width=minPW, max_pulse_width=maxPW)

while True:

    print("Set value range -1.0 to +1.0")
    for value in range(8, 13):
        value2 = (float(value)-10)/10
        servo.value = value2
        servo2.value = value2
        print(value2)
        sleep(0.5)

    print("Set value range +1.0 to -1.0")
    for value in range(13, 8, -1):
        value2 = (float(value)-10)/10
        servo.value = value2
        servo2.value = value2
        print(value2)
        sleep(0.5)
