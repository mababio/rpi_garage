from urllib import request, parse


def send_push_notification(message):
    token = "CIDEx7AGEiJBRERKNklQMlJNSEpaSkhSSEdOR1pIUEE0NUlQQUFNNENVIgIIAQ.kjUkfcqsKdw7KRH1RcS1u_PqtZyNqvXPNS-dj6b43Fg"
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + token, data=data)
    request.urlopen(req)


if __name__ == "__main__":
    send_push_notification('testing')
