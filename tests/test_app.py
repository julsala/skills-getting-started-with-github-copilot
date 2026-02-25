
"""Tests for the FastAPI application in src/app.py."""

from fastapi.responses import RedirectResponse

def test_root_redirects(client):
    # Arrange & Act (don't follow redirects)
    response = client.get("/", follow_redirects=False)
    # Assert that we received a redirect status code and proper Location header
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body


# POST /activities/{activity_name}/signup

def test_signup_success(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_nonexistent_activity(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": "a@b.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate(client):
    # first signup
    email = "duplicate@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    # second signup should fail
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


# DELETE /activities/{activity_name}/participants

def test_remove_participant_success(client):
    email = "removeme@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.delete("/activities/Chess Club/participants", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"


def test_remove_participant_nonexistent_activity(client):
    response = client.delete("/activities/Nonexistent/participants", params={"email": "a@b.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_not_signed_up(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "not@there.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
