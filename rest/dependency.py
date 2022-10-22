from infarstructure import MongoDBConfig, MongoDB


def inject():
    mongo_db = MongoDB(MongoDBConfig()).getDB("SlipVerification")
