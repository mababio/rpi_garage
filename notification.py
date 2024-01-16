<<<<<<< HEAD
import os
from os import environ
from urllib import request, parse

try:
    TOKEN = os.environ['CHANIFY_KEY']
except KeyError:
    print('notification.py::::: ERROR ------> missing env variables')
    raise


def send_push_notification(message):
    token = TOKEN
=======
from urllib import request, parse

def send_push_notification(message):
     #settings['production']['key']['chanify']
>>>>>>> 7891ba2 (pushed chanify code into notification.py)
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + token, data=data)
    request.urlopen(req)

<<<<<<< HEAD

if __name__ == "__main__":
    send_push_notification('testing')
=======
>>>>>>> 7891ba2 (pushed chanify code into notification.py)
