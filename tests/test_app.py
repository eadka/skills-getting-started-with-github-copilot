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


def test_student_can_unregister_from_activity():
    activity_name = "Chess Club"
    email = "remove.student@mergington.edu"

    participants = activities[activity_name]["participants"]
    original = list(participants)
    try:
        participants[:] = [e for e in participants if e != email]

        signup = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup.status_code == 200

        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        assert response.status_code == 200
        assert email not in participants
    finally:
        participants[:] = original
