from infrastructure import MongoDB,MongoDBConfig
def inject():
    mongo_db = MongoDB(MongoDBConfig()).getDB("SlipVerification")
