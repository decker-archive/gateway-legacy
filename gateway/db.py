import pymongo
import os
import dotenv

dotenv.load_dotenv()

client = pymongo.MongoClient(os.getenv('mongo_uri'))

_users = client.get_database('users', read_preference=pymongo.ReadPreference.SECONDARY)
_guilds = client.get_database('guilds', read_preference=pymongo.ReadPreference.SECONDARY)

members = _guilds.get_collection('members', read_preference=pymongo.ReadPreference.SECONDARY)
users = _users.get_collection('core', read_preference=pymongo.ReadPreference.SECONDARY)