from concurrent.futures import TimeoutError
from util import notification
import pytz
from google.cloud import pubsub_v1
from relay import garage
from datetime import datetime
from tinydb import TinyDB, Query

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
project_id = "ensure-dev-zone"
subscription_id = "garage-control-sub"
subscription_path = subscriber.subscription_path(project_id, subscription_id)

db = TinyDB('/home/mababio/app/db.json')
instance_ = Query()


def get_message_age(message):
    message_datetime_obj = datetime.strptime(str(message.publish_time).split('.')[0], "%Y-%m-%d %H:%M:%S")

    current_timestamp_utc_datetime_obj = datetime.now(pytz.UTC)
    current_timestamp_utc_datetime_obj_formatted = str(current_timestamp_utc_datetime_obj).split('.')[0]
    accepted_current_timestamp_utc_datetime_obj = datetime.strptime(current_timestamp_utc_datetime_obj_formatted,
                                                                    "%Y-%m-%d %H:%M:%S")

    timelapse = accepted_current_timestamp_utc_datetime_obj - message_datetime_obj
    return int(timelapse.total_seconds())  # this is in sec


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()
    db.clear_cache()
    current_value = db.search(instance_.type == 'limit')[0]['value']
    if current_value <= 0:
        notification.send_push_notification("Raspberry Pi ::::: Blocking pubsub")
    else:
        pubsub_message = message.data.decode()
        message_timelapse = get_message_age(message)
        if message_timelapse >= 5:
            notification.send_push_notification("Raspberry Pi ::::: pubsub message is more than 5 secs, so ignore")
        else:
            garage(pubsub_message)
            print(' Would of opened garage')
            notification.send_push_notification("Raspberry Pi :::::  Garage would of opened")


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

