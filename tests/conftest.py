import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.role import Role
from app.helpers.auth import hash_password

# Set environment variable for testing
os.environ["ENV"] = "testing"
print(f"ENV set to: {os.getenv('ENV')}")

# Load ENV Var from .env
load_dotenv()
print(".env loaded")

# Get DB URL
DATABASE_URL = os.getenv("DATABASE_URL_TEST")
print(f"DATABASE_URL_TEST from .env: {DATABASE_URL}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL_TEST not present in .env")

# Load Alembic configuration
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
print("Alembic configuration set")

# Run Alembic migrations
command.upgrade(alembic_cfg, "head")
print("Alembic migrations run")

# DB Config for tests
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("Testing database session configured")


# Override the get_db dependency to use the testing database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Define a fixture for the database session
@pytest.fixture(scope="session")
def db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    # Create a new database session
    db = TestingSessionLocal()
    try:
        # Yield the database session to the tests
        yield db
    finally:
        # Close the database session
        db.close()
        # Drop all tables in the database
        Base.metadata.drop_all(bind=engine)


# Define a fixture for the FastAPI test client
@pytest.fixture(scope="session")
def client():
    # Create a FastAPI test client
    with TestClient(app) as c:
        # Yield the test client to the tests
        yield c


# Define a fixture to clean the database
@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
        yield db
    finally:
        db.close()


# Define a fixture to create a contributor role
@pytest.fixture(scope="session")
def contributor_role(db: Session):
    role = db.query(Role).filter(Role.name == "contributor").first()
    if not role:
        role = Role(name="contributor", description="Contributor role")
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


# Define a fixture to create an admin role
@pytest.fixture(scope="session")
def admin_role(db: Session):
    role = db.query(Role).filter(Role.name == "admin").first()
    if not role:
        role = Role(name="admin", description="Administrator role")
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


# Define a fixture to create a user with contributor role
@pytest.fixture
def user(db: Session, contributor_role: Role):
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": hash_password("testpassword"),
        "role_id": contributor_role.id,
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    try:
        yield user
    finally:
        db.delete(user)
        db.commit()


# Define a fixture to create a second user with contributor role
@pytest.fixture
def user2(db: Session, contributor_role: Role):
    user_data = {
        "username": "test_user_2",
        "email": "test_2@example.com",
        "password": hash_password("testpassword"),
        "role_id": contributor_role.id,
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    try:
        yield user
    finally:
        db.delete(user)
        db.commit()


# Define a fixture to create an admin user
@pytest.fixture
def admin_user(db: Session, admin_role: Role):
    user_data = {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": hash_password("adminpassword"),
        "role_id": admin_role.id,
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    try:
        yield user
    finally:
        db.delete(user)
        db.commit()
