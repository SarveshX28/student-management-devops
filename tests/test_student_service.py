import pytest
from app import create_app
from app import services


@pytest.fixture
def client():
    services.students.clear()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_student(client):
    response = client.post(
        "/students",
        json={
            "id": "STU001",
            "name": "Test Student",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json["id"] == "STU001"


def test_get_student(client):
    services.add_student(
        "STU002",
        "Another Student",
        "another@example.com"
    )

    response = client.get("/students/STU002")

    assert response.status_code == 200
    assert response.json["name"] == "Another Student"


def test_student_not_found(client):
    response = client.get("/students/UNKNOWN")
    assert response.status_code == 404


def test_duplicate_student(client):
    services.add_student("STU003", "Test", "test@example.com")

    response = client.post(
        "/students",
        json={
            "id": "STU003",
            "name": "Duplicate",
            "email": "duplicate@example.com"
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "Student already exists"
