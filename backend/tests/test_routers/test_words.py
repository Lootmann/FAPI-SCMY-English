import pytest
from fastapi import status

from api.models.words import Word as WordModel
from api.schemas import words as word_schema
from tests.factory import WordFactory, random_string
from tests.init_client import client


class TestGetAllWords:
    def test_get_all_words_with_empty(self, client):
        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    def test_get_all_words(self, client):
        for _ in range(10):
            WordFactory.create_word(client, random_string(), random_string())

        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 10


class TestGetWord:
    def test_get_word(self, client):
        word_data = {"spell": "hello", "meaning": "こんにちは"}
        resp = client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_201_CREATED

        word_id = resp.json()["id"]

        resp = client.get(f"/words/{word_id}")
        assert resp.status_code == status.HTTP_200_OK

        word = word_schema.WordCreateResponse(**resp.json())
        assert word.spell == "hello"
        assert word.meaning == "こんにちは"

    def test_fail_to_get_words(self, client):
        resp = client.get("/words/128735")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestSearchWord:
    def test_search_word_with_both(self, client):
        resp = client.get("/words/search/?spell=a&meaning=b")
        assert resp.status_code == status.HTTP_200_OK

        WordFactory.create_word(client, spell="aZZ", meaning="ZZZ")
        WordFactory.create_word(client, spell="ZZZ", meaning="bZZ")
        WordFactory.create_word(client, spell="AZX", meaning="ZZX")
        WordFactory.create_word(client, spell="ZZX", meaning="BZX")

        resp = client.get("/words/search/?spell=a&meaning=b")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 4

        resp = client.get("/words/search/?spell=A&meaning=B")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 4

    def test_search_word_by_spell(self, client):
        resp = client.get("/words/search/?spell=a")
        assert resp.status_code == status.HTTP_200_OK

        WordFactory.create_word(client, spell="aaa", meaning="bbb")
        WordFactory.create_word(client, spell="AAZ", meaning="BBZ")

        resp = client.get("/words/search/?spell=a")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

        resp = client.get("/words/search/?spell=A")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

    def test_search_word_by_meaning(self, client):
        resp = client.get("/words/search/?meaning=b")
        assert resp.status_code == status.HTTP_200_OK

        WordFactory.create_word(client, spell="aaa", meaning="ccc")
        WordFactory.create_word(client, spell="AAZ", meaning="CCZ")

        resp = client.get("/words/search/?meaning=c")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

        resp = client.get("/words/search/?meaning=C")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

    def test_search_word_without_query(self, client):
        resp = client.get("/words/search/")
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestPostWords:
    def test_create_word(self, client):
        word_data = {"spell": "hello", "meaning": "こんにちは"}
        resp = client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_fail_to_create_word_with_invalid_body(self, client):
        word_data = {"spell": "hello", "translation": "こんにちは"}
        resp = client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        word_data = {"spelling": "hello", "meaning": "こんにちは"}
        resp = client.post("/words", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_try_to_create_duplicate_word(self, client):
        resp = client.post("/words", json={"spell": "hoge", "meaning": "hage"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/words", json={"spell": "hoge", "meaning": "hage"})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


class TestPatchWords:
    def test_patch_word(self, client):
        word = WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"spell": "updated", "meaning": "updated"}

        resp = client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] == "updated"
        assert resp_obj["meaning"] == "updated"

    def test_patch_word_with_only_spell(self, client):
        word = WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"spell": "updated"}

        resp = client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] != "spelling"
        assert resp_obj["spell"] == "updated"
        assert resp_obj["meaning"] != "updated"
        assert resp_obj["meaning"] == "meaning"

    def test_patch_word_with_only_meaning(self, client):
        word = WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {"meaning": "updated"}

        resp = client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["spell"] == "spelling"
        assert resp_obj["spell"] != "updated"
        assert resp_obj["meaning"] == "updated"
        assert resp_obj["meaning"] != "meaning"

    def test_patch_word_without_parameters(self, client):
        word = WordFactory.create_word(client, "spelling", "meaning")
        word_id = word.id
        word_data = {}

        resp = client.patch(f"/words/{word_id}", json=word_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_patch_word_with_wrong_id(self, client):
        word_data = {"spell": "updated", "meaning": "updated"}
        resp = client.patch(f"/words/287364", json=word_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteWord:
    def test_delete_word(self, client):
        word = WordFactory.create_word(client, "spelling", "meaning")

        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        word_id = word.id

        resp = client.delete(f"/words/{word_id}")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj == None

        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    def test_try_to_delete_word_with_wrong_id(self, client):
        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

        resp = client.delete(f"/words/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
