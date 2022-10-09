from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from urllib import request, parse
from control import garage

chanify = 'CIC8jp0GEiJBRERKNklQMlJNSEpaSkhSSEdOR1pIUEE0NUlQQUFNNENVIgIIAQ.WZeft-Bg2oKWAC7_3DSzh1vnwnLPH-kPUlqm0cM2WWg'
def send_push_notification(message):
     #settings['production']['key']['chanify']
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + token, data=data)
    request.urlopen(req)


# TODO(developer)
# project_id = "your-project-id"
# subscription_id = "your-subscription-id"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`

project_id = "ensure-dev-zone"
subscription_id = "garage-control-sub"
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    send_push_notification('mababio@@@@')
    garage()
    message.ack()

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
