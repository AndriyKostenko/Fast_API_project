import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.database import Base, get_db
from app.main import app_


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:changeme@db_test/postgres.db.test'


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)
    app_.dependency_overrides[get_db] = lambda: db
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app_.dependency_overrides[get_db] = lambda: db
    with TestClient(app_) as c:
        yield c
