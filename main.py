import os
from multiprocessing import Process
import time
import redis
from logs import Logger

logger = Logger(__name__)
try:
    from RPi import GPIO # pylint: disable=import-error
except RuntimeError:
    logger.fatal("Error importing RPi.GPIO! "
                 " This is probably because you need superuser privileges. "
                 "You can achieve this by using 'sudo' to run your script")
    raise

GARAGE_SENSOR_PIN = 4
GARAGE_CONTROL_PIN = 17
try:
    REDIS_HOST = os.environ['REDIS_HOST']
except KeyError:
    print('REDIS_HOST not set')
    raise


# TODO: May need to put some safety checks in here to
#  make sure garage does not go haywire if pub/sub goes crazy

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
                logger.info("Garage is open already! request to open has been ignored")
                r.publish('garage-state', 'opened')
            else:
                print("Opening Garage!")
                logger.info("Opening Garage!")
                r.publish('garage-state', 'opening')
                garage_relay()
                r.publish('garage-state', 'opened')
        elif message['data'] == 'close':
            if read_garage_door_sensor() != 1:
                logger.info("Garage is closed already! Request to closed has been ignored")
                r.publish('garage-state', 'closed')
            else:
                logger.info("Closing Garage!")
                r.publish('garage-state', 'closing')
                garage_relay()
                r.publish('garage-state', 'closed')
        elif message['data'] == 1:
            logger.info('got 1 returned meaning pub/sub has been initialized')
        else:
            logger.info(f'Invalid message {message}')


def garage_relay():
    """
    Low level controls to open/close garage
    """
    logger.info('TESTING >>>>>> doing action')
    return 1
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
    val = GPIO.input(GARAGE_SENSOR_PIN)
    logger.info(f"read state is: {val}")
    return val


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
    logger.info(f'RPI::: Sending Garage state to redis::: Garage State: {garage_state}')


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
