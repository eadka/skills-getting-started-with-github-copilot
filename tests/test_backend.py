from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_expected_structure():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant_and_rejects_duplicates():
    activity_name = "Chess Club"
    email = "backend.test@mergington.edu"

    original = list(activities[activity_name]["participants"])
    try:
        activities[activity_name]["participants"] = [
            participant for participant in activities[activity_name]["participants"] if participant != email
        ]

        first = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert first.status_code == 200
        assert email in activities[activity_name]["participants"]

        second = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert second.status_code == 400
        assert activities[activity_name]["participants"].count(email) == 1
    finally:
        activities[activity_name]["participants"] = original


def test_unregister_removes_participant():
    activity_name = "Chess Club"
    email = "backend.remove@mergington.edu"

    original = list(activities[activity_name]["participants"])
    try:
        activities[activity_name]["participants"] = [
            participant for participant in activities[activity_name]["participants"] if participant != email
        ]

        signup = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup.status_code == 200

        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert "Unregistered" in response.json()["message"]
    finally:
        activities[activity_name]["participants"] = original
