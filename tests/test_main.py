from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_employees():
    r = client.get("/employees")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_employee_success():
    r = client.get("/employees/Rahul")
    assert r.status_code == 200
    assert r.json()["name"] == "Rahul"


def test_get_employee_404():
    assert client.get("/employees/Ravi").status_code == 404


def test_invalid_salary():
    r = client.post(
        "/employees", json={"name": "Sam", "department": "IT", "salary": -5}
    )
    assert r.status_code == 422


def test_empty_name():
    r = client.post("/employees", json={"name": "", "department": "IT", "salary": 1000})
    assert r.status_code == 422


def test_create_employee():
    r = client.post(
        "/employees", json={"name": "Sam", "department": "IT", "salary": 5000}
    )
    assert r.status_code == 201
