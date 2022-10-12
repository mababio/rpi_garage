import RPi.GPIO as GPIO
import time, sys
import util.notification as notification
from tinydb import TinyDB, Query
import requests
from util.config import settings

db = TinyDB('/home/mababio/app/db.json')
instance_ = Query()


def is_garage_open():
    return False if requests.post(settings['production']['URL']['myq_garage'], json={"isopen": ''}).json()['isopen'] \
                    == 'closed' else True


def garage(pubsub_message):
    pubsub_str = str(pubsub_message)
    if pubsub_str == "open" or pubsub_str == "close":
        notification.send_push_notification('Raspberry Pi is interfacing with Garage')
        if not is_garage_open():
            notification.send_push_notification(str(db.search(instance_.type == 'limit')[0]['value']))
            notification.send_push_notification("Raspberry Pi  ::::: Opening Garage door")
            garage_relay()
        else:
            notification.send_push_notification("Closing garage is disabled for now")
    else:
        notification.send_push_notification("pubsub message was not open or close")


def garage_relay():
    your_board_gpio = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(your_board_gpio, GPIO.OUT)
    GPIO.setwarnings(False)
    print("on")
    GPIO.output(your_board_gpio, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(your_board_gpio, GPIO.LOW)
    print("off")
    GPIO.cleanup(your_board_gpio)


if __name__ == "__main__":
    print(is_garage_open())
