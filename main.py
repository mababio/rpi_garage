from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from urllib import request, parse
from relay import garage
import util.notification as notification
import base64


timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
project_id = "ensure-dev-zone"
subscription_id = "garage-control-sub"
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()
    pubsub_message = message.data.decode()
    garage(pubsub_message)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()#timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

