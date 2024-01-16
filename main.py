import os
from multiprocessing import Process
import time
import RPi.GPIO as GPIO
import redis
import notification

GARAGE_SENSOR_PIN = 17
GARAGE_CONTROL_PIN = 4

try:
    REDIS_HOST = os.environ['REDIS_HOST']
except KeyError:
    print('main.py::::: ERROR ------> missing env variables')
    raise


def listener():
    """
    Listen to redis channel for garage door open/close request
    """
    r = redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True
    )

    mobile = r.pubsub()
    mobile.subscribe('garage-request')

    for message in mobile.listen():
        if message['data'] == 'open':
            if read_garage_door_sensor() == 1:
                print("Garage is open already! request to open has been ignored")
                notification.send_push_notification("Garage is open already! request to open has been ignored")
                r.publish('garage-state', 'opened')
            else:
                print("Opening Garage!")
                notification.send_push_notification("Opening Garage!")
                r.publish('garage-state', 'opening')
                garage_relay()
                r.publish('garage-state', 'opened')
        elif message['data'] == 'close':
            if read_garage_door_sensor() != 1:
                print("Garage is closed already! Request to closed has been ignored")
                notification.send_push_notification("Garage is closed already! Request to closed has been ignored")
                r.publish('garage-state', 'closed')
            else:
                print("Closing Garage!")
                notification.send_push_notification("Closing Garage!")
                r.publish('garage-state', 'closing')
                garage_relay()
                r.publish('garage-state', 'closed')
        else:
            print(f'Invalid message {message}')
            notification.send_push_notification(f'Invalid message {message}')


def garage_relay():
    """
    Low level controls to open/close garage
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GARAGE_CONTROL_PIN, GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.output(GARAGE_CONTROL_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GARAGE_CONTROL_PIN, GPIO.LOW)
    GPIO.cleanup(GARAGE_CONTROL_PIN)


def read_garage_door_sensor():
    """
    Read garage door sensor
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GARAGE_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return GPIO.input(GARAGE_SENSOR_PIN)


def send_state_to_redis(garage_state):
    """
    Send garage state to redis
    """
    r = redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True
    )
    r.set('garage-state', garage_state)
    notification.send_push_notification(f'RPI::: Sending Garage state to redis::: Garage State: {garage_state}')


def read_and_send_state_to_redis():
    """
    Read garage door sensor and send state to redis
    """
    while True:
        state = read_garage_door_sensor()
        if state == 0:
            send_state_to_redis('closed')
        else:
            send_state_to_redis('opened')
        time.sleep(2)


if __name__ == '__main__':
    p1 = Process(target=listener)
    p2 = Process(target=read_and_send_state_to_redis)
    p1.start()
    p2.start()
