from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_student_cannot_register_twice_for_same_activity():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    # ensure a clean starting state for this test
    participants = activities[activity_name]["participants"]
    original = list(participants)
    try:
        participants[:] = [e for e in participants if e != email]

        first = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert first.status_code == 200

        second = client.post(f"/activities/{activity_name}/signup?email={email}")

        assert second.status_code == 400
        assert participants.count(email) == 1
    finally:
        participants[:] = original
