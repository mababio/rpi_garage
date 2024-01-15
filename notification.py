from os import environ
from urllib import request, parse

TOKEN = environ.get('CHANIFY_KEY')


def send_push_notification(message):
    
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + , data=data)
    request.urlopen(req)


if __name__ == "__main__":
    send_push_notification('testing')
