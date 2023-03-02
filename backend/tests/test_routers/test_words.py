import pytest
from fastapi import status

from api.models.words import Word as WordModel
from api.schemas import words as word_schema
from tests.factory import WordFactory, random_string
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllWords:
    async def test_get_all_words_with_empty(self, client):
        resp = await client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    async def test_get_all_words(self, client):
        for _ in range(10):
            await WordFactory.create_word(client, random_string(), random_string())

        resp = await client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 10


@pytest.mark.asyncio
class TestGetWord:
    async def test_get_word(self, client):
        word_data = {"spell": "hello", "meaning": "こんにちは"}
        resp = await client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_201_CREATED

        word_id = resp.json()["id"]

        resp = await client.get(f"/words/{word_id}")
        assert resp.status_code == status.HTTP_200_OK

        word = word_schema.WordCreateResponse(**resp.json())
        assert word.spell == "hello"
        assert word.meaning == "こんにちは"

    async def test_fail_to_get_words(self, client):
        resp = await client.get("/words/128735")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestSearchWord:
    async def test_search_word_with_both(self, client):
        resp = await client.get("/words/search/?spell=a&meaning=b")
        assert resp.status_code == status.HTTP_200_OK

        await WordFactory.create_word(client, spell="aZZ", meaning="ZZZ")
        await WordFactory.create_word(client, spell="ZZZ", meaning="bZZ")
        await WordFactory.create_word(client, spell="AZX", meaning="ZZX")
        await WordFactory.create_word(client, spell="ZZX", meaning="BZX")

        resp = await client.get("/words/search/?spell=a&meaning=b")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 4

        resp = await client.get("/words/search/?spell=A&meaning=B")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 4

    async def test_search_word_by_spell(self, client):
        resp = await client.get("/words/search/?spell=a")
        assert resp.status_code == status.HTTP_200_OK

        await WordFactory.create_word(client, spell="aaa", meaning="bbb")
        await WordFactory.create_word(client, spell="AAZ", meaning="BBZ")

        resp = await client.get("/words/search/?spell=a")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

        resp = await client.get("/words/search/?spell=A")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

    async def test_search_word_by_meaning(self, client):
        resp = await client.get("/words/search/?meaning=b")
        assert resp.status_code == status.HTTP_200_OK

        await WordFactory.create_word(client, spell="aaa", meaning="ccc")
        await WordFactory.create_word(client, spell="AAZ", meaning="CCZ")

        resp = await client.get("/words/search/?meaning=c")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

        resp = await client.get("/words/search/?meaning=C")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

    async def test_search_word_without_query(self, client):
        resp = await client.get("/words/search/")
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


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

    async def test_try_to_create_duplicate_word(self, client):
        resp = await client.post("/words", json={"spell": "hoge", "meaning": "hage"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.post("/words", json={"spell": "hoge", "meaning": "hage"})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
class TestPatchWords:
    async def test_patch_word(self, client):
        word = await WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"spell": "updated", "meaning": "updated"}

        resp = await client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] == "updated"
        assert resp_obj["meaning"] == "updated"

    async def test_patch_word_with_only_spell(self, client):
        word = await WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"spell": "updated"}

        resp = await client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] != "spelling"
        assert resp_obj["spell"] == "updated"
        assert resp_obj["meaning"] != "updated"
        assert resp_obj["meaning"] == "meaning"

    async def test_patch_word_with_only_meaning(self, client):
        word = await WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"meaning": "updated"}

        resp = await client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] == "spelling"
        assert resp_obj["spell"] != "updated"
        assert resp_obj["meaning"] == "updated"
        assert resp_obj["meaning"] != "meaning"

    async def test_patch_word_without_parameters(self, client):
        word = await WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {}

        resp = await client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_patch_word_with_wrong_id(self, client):
        word_data = {"spell": "updated", "meaning": "updated"}
        resp = await client.patch(f"/words/287364", json=word_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestDeleteWord:
    async def test_delete_word(self, client):
        word = await WordFactory.create_word(client, "spelling", "meaning")

        resp = await client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        word_id = word.id

        resp = await client.delete(f"/words/{word_id}")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj == None

        resp = await client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    async def test_try_to_delete_word_with_wrong_id(self, client):
        resp = await client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

        resp = await client.delete(f"/words/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
