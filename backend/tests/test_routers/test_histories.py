import pytest
from fastapi import status

from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllHistoires:
    async def test_get_all_histories(self, client):
        resp = await client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []


@pytest.mark.asyncio
class TestGetHistory:
    async def test_get_history(self, client):
        resp = await client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED

        history_id = resp.json()["id"]
        resp = await client.get(f"/histories/{history_id}")
        assert resp.status_code == status.HTTP_200_OK

    async def test_get_history_wrong_id(self, client):
        resp = await client.get("/histories/1")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestPostHistory:
    async def test_post_history(self, client):
        resp = await client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

        resp = await client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["id"] == 1

        resp = await client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1


@pytest.mark.asyncio
class TestDeleteHistory:
    async def test_delete_history(self, client):
        resp = await client.post("/histories")
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        history_id = resp.json()[0]["id"]
        resp = await client.delete(f"/histories/{history_id}")

        resp = await client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    async def test_delete_history_with_wrong_id(self, client):
        resp = await client.delete("/histories/9837124")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
