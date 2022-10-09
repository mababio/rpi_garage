import RPi.GPIO as GPIO
import time, sys


def garage1():
    print('fffffffffffffff')

def garage():
    your_board_gpio = 4

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(your_board_gpio,GPIO.OUT)
    GPIO.setwarnings(False)

    print("on")
    GPIO.output(your_board_gpio,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(your_board_gpio,GPIO.LOW)
    print("off")
    GPIO.cleanup(your_board_gpio)


if __name__ == "__main__":
    garage()
