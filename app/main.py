from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.routers import user, role, publication
from seeds.roles import seed_roles
from seeds.users import seed_admin_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    seed_roles(db)
    seed_admin_user(db)
    db.close()


app.include_router(user.router, tags=["users"])
app.include_router(role.router, tags=["roles"])
app.include_router(publication.router, tags=["publications"])
