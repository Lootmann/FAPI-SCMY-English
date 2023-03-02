from fastapi import status

from tests.init_client import client


class TestGetAllHistoires:
    def test_get_all_histories(self, client):
        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []


class TestGetHistory:
    def test_get_history(self, client):
        resp = client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED

        history_id = resp.json()["id"]
        resp = client.get(f"/histories/{history_id}")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_history_wrong_id(self, client):
        resp = client.get("/histories/1")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestPostHistory:
    def test_post_history(self, client):
        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

        resp = client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["id"] == 1

        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1


class TestDeleteHistory:
    def test_delete_history(self, client):
        resp = client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        history_id = resp.json()[0]["id"]
        resp = client.delete(f"/histories/{history_id}")

        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    def test_delete_history_with_wrong_id(self, client):
        resp = client.delete("/histories/9837124")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
