import json
import pymongo
from pymongo.server_api import ServerApi
from util import notification
from google.cloud import pubsub_v1
from util.config import settings


class DBClient:

    def __init__(self):
        try:
REMOVED
            self.tesla_database = client['tesla']
        except Exception as e:
            raise

    def get_tesla_database(self):
        try:
            return self.tesla_database
        except Exception as e:
            raise

    def get_tesla_location_is_home_value(self):
        return self.tesla_database['tesla_location'].find_one({"_id": "current"})['is_home']

    def get_ifttt_trigger_lock(self):
        return self.tesla_database['tesla_trigger'].find_one()['lock']

    def get_door_close_status(self):
        return self.tesla_database['garage'].find_one()['closed_reason']

    def get_door_open_status(self):
        return self.tesla_database['garage'].find_one({'_id': 'garage'})['opened_reason']

    def get_saved_location(self):
        return self.tesla_database['tesla_location'].find_one({'_id': 'current'})
