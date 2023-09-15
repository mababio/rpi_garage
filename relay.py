import RPi.GPIO as GPIO
import time, sys
import util.notification as notification
from tinydb import TinyDB, Query
import requests
from util.config import settings

db = TinyDB('/home/mababio/app/db.json')
instance_ = Query()


def is_garage_open():
    return False if requests.Session().post(settings['production']['URL']['myq_garage'], json={"isopen": ''}).json()['isopen'] \
                    == 'closed' else True


def garage(pubsub_message):
    """
        Wrapper around the low level control for garage.
    :param pubsub_message: string pub/sub message to either open or close garage door
    """
    pubsub_str = str(pubsub_message)
    if pubsub_str == "open" or pubsub_str == "close":
        if not is_garage_open():
            garage_relay()
            notification.send_push_notification("Raspberry Pi  ::::: Opening Garage door")
        else:
            notification.send_push_notification("Closing garage is disabled for now")
    else:
        notification.send_push_notification("pubsub message was not open or close")


def garage_relay():
    """
    Low level controls to open/close garage
    """
    your_board_gpio = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(your_board_gpio, GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.output(your_board_gpio, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(your_board_gpio, GPIO.LOW)
    GPIO.cleanup(your_board_gpio)


if __name__ == "__main__":
    your_board_gpio = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(your_board_gpio, GPIO.OUT)

    state = GPIO.input(4)

    if state:
        print('yes')
    else:
        print('no')

