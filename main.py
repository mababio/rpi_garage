import random
from paho.mqtt import client as mqtt_client
from util.config import settings
import RPi.GPIO as GPIO
import time, sys
from util import validator

broker = settings['mqtt']['broker']
port = 8883
topic = "garage/command"
client_id = f'garage-command-{random.randint(0, 100)}'
username = settings['mqtt']['username']
password = settings['mqtt']['password']


# TODO: Maybe set up logging sink
def connect_mqtt() -> mqtt_client:
    """
    Connecting to mqtt  garage topic
    :return: mqtt client object
    """

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.payload.decode() == "open" and not validator.garage_is_open():
            garage_relay()
        elif msg.payload.decode() == "closed" and validator.garage_is_open():
            garage_relay()

    client.subscribe(topic)
    client.on_message = on_message

    # notification.send_push_notification("Raspberry Pi  ::::: Opening Garage door")


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


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
