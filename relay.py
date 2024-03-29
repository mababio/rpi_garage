import RPi.GPIO as GPIO
import time, sys
import util.notification as notification
from tinydb import TinyDB, Query 
db = TinyDB('/home/mababio/app/db.json') 
instance_ = Query() 
 
 
def garage(pubsub_message):
    db.clear_cache()
    current_value =  db.search(instance_.type == 'limit')[0]['value'] 
    pubsub_str =  str(pubsub_message)
    if pubsub_str ==  "open" or pubsub_str == "close":
        if current_value != 0 :
            notification.send_push_notification('Raspberry Pi is interfacing with Garage')
            new_value = int(current_value) - 1
            db.update({'value': new_value }, instance_.type== 'limit')
            notification.send_push_notification(str( db.search(instance_.type == 'limit')[0]['value']))
            garage_relay()
        else: 
            print('Limit has been reached')
            notification.send_push_notification('Appears the Garage has been Open too many times via automation!!! Has been temporary  disabled')
    else:
        notification.send_push_notification("pubsub message was not open or close")

def garage_relay():
    your_board_gpio = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(your_board_gpio,GPIO.OUT)
    GPIO.setwarnings(False)
    print("on")
    GPIO.output(your_board_gpio,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(your_board_gpio,GPIO.LOW)
    print("off")
    GPIO.cleanup(your_board_gpio)


if __name__ == "__main__":
    garage()
