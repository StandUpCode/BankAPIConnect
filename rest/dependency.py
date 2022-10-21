from infarstructure.mongo import MongoDB, MongoDBConfig


async def inject():
    mongo_db = MongoDB(MongoDBConfig())

    return mongo_db.getDB("SlipVerification")
