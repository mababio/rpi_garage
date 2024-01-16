import RPi.GPIO as GPIO
import time, sys
import notification

def garage():
    print('fffffffffffffff')
    notification.send_push_notification('garage closing ... testing')

def garage_hold():
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
