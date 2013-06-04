import pymongo
import pprint
conn = pymongo.Connection("localhost", 27017)
dbnames = conn.database_names()
print "Databases:"
pprint.pprint(dbnames, indent=4)

db = conn["PhoneCat"]
collections = db.collection_names()

print "Collections:"
pprint.pprint(collections, indent=4)
coll = db.phones
print db.phones
print "Phone _id(s)"
pprint.pprint(map(lambda x : x.get('_id', 'XXX'), coll.find()), indent=4)
phone = coll.find_one({"_id": 'nexus-s'})
pprint.pprint(phone, indent=4)