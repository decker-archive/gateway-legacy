import pymongo
import os
import dotenv
import asyncio
import motor.core
import motor.motor_asyncio

dotenv.load_dotenv()

loop = asyncio.new_event_loop()

client: motor.core.AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv('mongo_uri'), io_loop=loop
)

_users: motor.core.AgnosticDatabase = client.get_database(
    'users', read_preference=pymongo.ReadPreference.SECONDARY
)
_guilds: motor.core.AgnosticDatabase = client.get_database(
    'guilds', read_preference=pymongo.ReadPreference.SECONDARY
)

members: motor.core.AgnosticCollection = _guilds.get_collection(
    'members', read_preference=pymongo.ReadPreference.SECONDARY
)
users: motor.core.AgnosticCollection = _users.get_collection(
    'core', read_preference=pymongo.ReadPreference.SECONDARY
)
guilds: motor.core.AgnosticCollection = _guilds.get_collection('core')
channels: motor.core.AgnosticCollection = _guilds.get_collection('channels')
presences: motor.core.AgnosticCollection = _users.get_collection('presences')
