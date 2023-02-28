import pytest
from fastapi import status

from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllWords:
    async def test_get_all_words(self, client):
        resp = await client.get("/words")
        print(resp.json())
        assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestPostWords:
    async def test_create_word(self, client):
        word_data = {"spell": "hello", "meaning": "こんにちは"}
        resp = await client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_fail_to_create_word_with_invalid_body(self, client):
        word_data = {"spell": "hello", "translation": "こんにちは"}
        resp = await client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        word_data = {"spelling": "hello", "meaning": "こんにちは"}
        resp = await client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
