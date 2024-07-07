from fastapi import FastAPI
from routers.listeners_routers import router as listener_router
from routers.notifications_routers import router as notify_router

app = FastAPI()

app.include_router(listener_router)
app.include_router(notify_router)