import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.main import app
from app.database import Base, get_db

# Load ENV Var from .env
load_dotenv()

# Get DB URL
DATABASE_URL = os.getenv("DATABASE_URL_TEST")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL_TEST not present in .env")


# DB Config for tests
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define a fixture for the database session
@pytest.fixture(scope="module")
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
@pytest.fixture(scope="module")
def client():
    # Override the get_db dependency to use the testing database session
    def override_get_db():
        try:
            # Create a new database session
            db = TestingSessionLocal()
            # Yield the database session to the tests
            yield db
        finally:
            # Close the database session
            db.close()

    # Override the get_db dependency in the FastAPI app
    app.dependency_overrides[get_db] = override_get_db
    # Create a FastAPI test client
    with TestClient(app) as c:
        # Yield the test client to the tests
        yield c
