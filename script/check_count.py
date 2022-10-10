from tinydb import TinyDB, Query 
db = TinyDB('/home/mababio/app/db.json') 
instance_ = Query() 
 

value = db.search(instance_.type == "limit")[0]['value'] 
print(value)
