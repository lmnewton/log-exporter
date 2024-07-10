from fastapi.testclient import TestClient
import os

from app.main import app
from app.main import READ_LOCATION

client = TestClient(app)

os.environ[READ_LOCATION] = f"{os.getcwd()}/resources"


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_read_missingfile():
    response = client.get("/logs/fakefile?lines_to_read=5")
    assert response.status_code == 404


def test_missing_params():
    response = client.get("/logs/fakefile")
    assert response.status_code == 400


def test_bad_params():
    response = client.get("/logs/buffered.testlog?lines_to_read=-1")
    assert response.status_code == 400

    response = client.get("/logs/buffered.testlog?lines_to_read=five")
    assert response.status_code == 400


def test_read():
    response = client.get("/logs/buffered.testlog?lines_to_read=5")
    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 5

    response = client.get("/logs/buffered.testlog?lines_to_read=5000")
    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 32

    response = client.get("/logs/buffered.testlog?lines_to_read=50&search_term=C")
    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 23


def test_subdir_read():
    subdir = "test/test.testlog"
    response = client.get(f"/logs/{subdir}?lines_to_read=50&search_term=1")
    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 3
