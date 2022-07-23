import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import jwt


from app.db.database import Base, get_db
from app.main import app_
from app.security.security import JWT_SECRET_KEY, ALGORITHM

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:changeme@db_test/postgres.db.test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app_.dependency_overrides[get_db] = override_get_db
    yield AsyncClient(app=app_, base_url="http://test")


@pytest.fixture
def auth_client(client):
    to_encode = {"sub": 'test@mail.com'}
    test_token = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token}"}
    return client


@pytest.fixture
def auth_client_again(client):
    to_encode = {"sub": 'quiz@mail.com'}
    test_token = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token}"}
    return client