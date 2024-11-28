import uvicorn
from fastapi import FastAPI

from routers.rest_router import rest_router
from routers.ws_router import ws_router

app = FastAPI()

app.include_router(rest_router)
app.include_router(ws_router)

uvicorn.run(app, port=8080)
