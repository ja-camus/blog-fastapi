import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv
from app.main import app
from app.database import Base
from app.models import User

# Load ENV Var from .env
load_dotenv()

# Get DB URL
DATABASE_URL = os.getenv("DATABASE_URL_TEST")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not present in .env")

# Load Alembic configuration
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
alembic_cfg.set_main_option("script_location", "alembic")

# Run Alembic migrations
command.upgrade(alembic_cfg, "head")

# DB Config for tests
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define get_db inside conftest.py
def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    # Override the get_db dependency to use the testing database session
    app.dependency_overrides[get_db] = get_db
    # Create a FastAPI test client
    with TestClient(app) as c:
        # Yield the test client to the tests
        yield c

# Define a fixture to clean User Table
@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
        yield db
    finally:
        db.close()


# Define a fixture to create User
@pytest.fixture
def user():
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "testpassword",
    }

    db = TestingSessionLocal()

    user = User(**user_data)
    db.add(user)
    db.commit()
    try:
        yield user
    finally:
        db.delete(user)
        db.commit()
        db.close()
