import random
from paho.mqtt import client as mqtt_client
from util.config import settings
from relay import garage_relay

broker = settings['mqtt']['broker']
port = 8883
topic = "garage/command"
# generate client ID with pub prefix randomly
client_id = f'garage-command-{random.randint(0, 100)}'
username = settings['mqtt']['username']
password = settings['mqtt']['password']


def connect_mqtt() -> mqtt_client:
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
        if msg.payload.decode == "open":
            garage_relay()
        elif msg.payload.decode == "closed":
            # TODO: need to put a checker in here for current garage status
            garage_relay()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
