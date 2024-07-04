from fastapi import FastAPI
from routers.listeners_routers import router as listener_router

app = FastAPI()

app.include_router(listener_router)