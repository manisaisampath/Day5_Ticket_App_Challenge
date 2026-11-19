import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404

def test_tickets_are_sorted_by_priority(client):
    response = client.get("/api/tickets")

    priorities = [
        ticket["priority"]
        for ticket in response.get_json()
    ]

    assert priorities == ["High", "High", "Medium", "Medium", "Low"]
def test_empty_title_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "title": "",
            "description": "Testing empty title",
            "category": "Hardware",
            "priority": "High"
        }
    )

    assert response.status_code == 400
def test_unknown_category_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "title": "Printer jam",
            "category": "Furniture"
        }
    )

    assert response.status_code == 400
def test_unknown_priority_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "title": "Printer jam",
            "category": "Hardware",
            "priority": "Urgent"
        }
    )

    assert response.status_code == 400
def test_unknown_status_returns_400(client):
    response = client.patch(
        "/api/tickets/1/status",
        json={"status": "Pending"}
    )

    assert response.status_code == 400
def test_updating_unknown_ticket_returns_404(client):
    response = client.patch(
        "/api/tickets/999/status",
        json={"status": "Resolved"}
    )

    assert response.status_code == 404
def test_missing_title_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "description": "Testing missing title",
            "category": "Hardware",
            "priority": "High"
        }
    )

    assert response.status_code == 400
def test_missing_title_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "description": "Testing missing title",
            "category": "Hardware",
            "priority": "High"
        }
    )

    assert response.status_code == 400


# Add your own tests below: one failing test for each bug you find,
# plus at least 5 negative tests.
