import pytest
from app import create_app
from app import services


@pytest.fixture
def client():
    services.students.clear()
    services.courses.clear()
    services.enrollments.clear()
    services.marks.clear()

    services.add_student(
        "STU001",
        "Test Student",
        "test@example.com"
    )

    services.add_course(
        "AIML101",
        "Artificial Intelligence",
        4
    )

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_add_marks(client):
    response = client.post(
        "/marks",
        json={
            "student_id": "STU001",
            "course_id": "AIML101",
            "marks": 85
        }
    )

    assert response.status_code == 201
    assert response.json["marks"] == 85


def test_invalid_marks(client):
    response = client.post(
        "/marks",
        json={
            "student_id": "STU001",
            "course_id": "AIML101",
            "marks": 110
        }
    )

    assert response.status_code == 400


def test_marks_for_unknown_student(client):
    response = client.post(
        "/marks",
        json={
            "student_id": "UNKNOWN",
            "course_id": "AIML101",
            "marks": 85
        }
    )

    assert response.status_code == 400


def test_calculate_gpa(client):
    services.add_marks("STU001", "AIML101", 85)

    response = client.get("/students/STU001/gpa")

    assert response.status_code == 200
    assert response.json["gpa"] == 8.5


def test_gpa_for_unknown_student(client):
    response = client.get("/students/UNKNOWN/gpa")
    assert response.status_code == 404
