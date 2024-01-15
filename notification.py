from urllib import request, parse
from util.config import settings


def send_push_notification(message):
    token = "***REMOVED***"
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + token, data=data)
    request.urlopen(req)


if __name__ == "__main__":
    send_push_notification('testing')
