from django.test import Client


def test_health_endpoint_ok():
    client = Client()
    res = client.get("/_health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
