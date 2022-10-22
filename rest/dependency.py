from Config import SCBConfig
from adapter import SCBAPI_Service

from infarstructure import MongoDBConfig, MongoDB


def inject():
    mongo_db = MongoDB(MongoDBConfig()).getDB("SlipVerification")
