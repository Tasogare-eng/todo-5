from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_crud_flow():
    # create
    payload = {
        "title": "最初のタスク",
        "description": "説明",
        "status": "todo",
        "priority": "medium",
        "dueDate": None,
    }
    r = client.post("/api/tasks", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    task_id = data["id"]
    assert data["title"] == payload["title"]

    # list
    r = client.get("/api/tasks")
    assert r.status_code == 200
    items = r.json()
    assert any(t["id"] == task_id for t in items)

    # get
    r = client.get(f"/api/tasks/{task_id}")
    assert r.status_code == 200

    # update (PUT)
    upd = payload | {"title": "更新タイトル"}
    r = client.put(f"/api/tasks/{task_id}", json=upd)
    assert r.status_code == 200
    assert r.json()["title"] == "更新タイトル"

    # status filter
    r = client.get("/api/tasks", params={"status": "todo"})
    assert r.status_code == 200

    # delete
    r = client.delete(f"/api/tasks/{task_id}")
    assert r.status_code == 204

    # get 404
    r = client.get(f"/api/tasks/{task_id}")
    assert r.status_code == 404


def test_validation_title_empty():
    r = client.post(
        "/api/tasks",
        json={
            "title": " ",
            "description": None,
            "status": "todo",
            "priority": "medium",
            "dueDate": None,
        },
    )
    assert r.status_code in (400, 422)
