from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router
from app.routers import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(user.router, prefix="/api/v1", tags=["users"])
