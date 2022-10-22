from fastapi import FastAPI

from . import dependency


async def startup(app: FastAPI):

    app.state.registry = dependency.inject()


async def shutdown(app: FastAPI):
    pass
