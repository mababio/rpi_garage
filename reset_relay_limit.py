from tinydb import TinyDB, Query 
from util.config import settings

db = TinyDB('/home/mababio/app/db.json') 
instance_ = Query() 
 
 
def reset_relay_limit():
    db.upsert({"type":"limit", "value": settings["production"]["limits"]["relay_limits"]}, instance_.type == "limit")



if __name__ == "__main__":
    reset_relay_limit()
