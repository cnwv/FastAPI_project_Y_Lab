import pytest
from fastapi.testclient import TestClient

from config import db
from config import sync_engine
from main import app
from src.api.CRUD.schemas import metadata


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert db.DB_NAME == "postgres-test"
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)


@pytest.fixture(scope="function")
def client():
    with TestClient(app=app) as client:
        yield client
