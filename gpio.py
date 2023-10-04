import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
while True:
    if(GPIO.input(7) == 1):
        os.system("sudo shutdown -hP now")
        print("System herunterfahren")

GPIO.cleanup()
