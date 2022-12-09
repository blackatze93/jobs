import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db

from dotenv import load_dotenv
load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT_TEST')

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_pass, db_host, db_port, db_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    json_test = {
        "first_name": "Test Name",
        "last_name": "Test Last",
        "email": "un.test.no.hace.mal@gmail.com",
        "years_previous_experience": 5,
        "skills": [
            {
                "Python": 1
            },
            {
                "NoSQL": 2
            }
        ]
    }
    response = client.post(
        "/users/",
        json=json_test
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "un.test.no.hace.mal@gmail.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "un.test.no.hace.mal@gmail.com"
    assert data["id"] == user_id