from functools import partial

from fastapi import FastAPI

from . import endpoint
from .event_handler import startup, shutdown


def create_app():
    fast_app = FastAPI(title='BankAPI Connect')

    fast_app.add_event_handler('startup', func=partial(startup, app=fast_app))
    fast_app.add_event_handler('shutdown', func=partial(shutdown, app=fast_app))
    return fast_app


app = create_app()


@app.get("/")
async def index():
    return {"message": "BANK API CONNECT v0.01"}


app.include_router(endpoint.slip_api, prefix='/api/v1/slip', tags=['slip'])
