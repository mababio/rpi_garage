from urllib import request, parse

chanify = 'CIC8jp0GEiJBRERKNklQMlJNSEpaSkhSSEdOR1pIUEE0NUlQQUFNNENVIgIIAQ.WZeft-Bg2oKWAC7_3DSzh1vnwnLPH-kPUlqm0cM2WWg'
def send_push_notification(message):
     #settings['production']['key']['chanify']
    message_json = {'text': message}
    data = parse.urlencode(message_json).encode()
    req = request.Request("https://api.chanify.net/v1/sender/" + , data=data)
    request.urlopen(req)

