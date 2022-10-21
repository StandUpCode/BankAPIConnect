from fastapi import FastAPI

import dependency


async def startup(app: FastAPI):
    mongo = dependency.inject()
    app.state.mongo_db = mongo


async def shutdown(app: FastAPI):
    app.state.mongo_db.close()
