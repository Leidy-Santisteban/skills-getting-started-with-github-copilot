import copy

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)
INITIAL_ACTIVITIES = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_get_activities_returns_all_activities():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_creates_new_participant_successfully():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_bad_request():
    # Arrange
    reset_activities()
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_success():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_not_found():
    # Arrange
    reset_activities()
    email = "missing@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
