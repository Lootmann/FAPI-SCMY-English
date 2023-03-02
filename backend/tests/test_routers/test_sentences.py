import pytest
from fastapi import status

from api.models.sentences import Sentence as SentenceModel
from api.schemas import sentences as sencente_schema
from tests.factory import SentenceFactory, random_string
from tests.init_client import client


class TestGetAllSentences:
    def test_get_all_sentences_with_empty(self, client):
        resp = client.get("/sentences")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    def test_get_all_sentences(self, client):
        for _ in range(100):
            SentenceFactory.create_sentence(client, random_string(), random_string())

        resp = client.get("/sentences")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 100


class TestGetSentence:
    def test_get_sentence(self, client):
        sentence = SentenceFactory.create_sentence(
            client, random_string(), random_string()
        )

        resp = client.get(f"/sentences/{sentence.id}")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()

        assert sentence.sentence == resp_obj["sentence"]
        assert sentence.translation == resp_obj["translation"]

    def test_fail_to_get_sentence(self, client):
        resp = client.get("/sentences/98734")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestPOSTSentence:
    def test_create_sentence(self, client):
        sentence_data = {"sentence": "hello, world", "translation": "こんにちは、せかい"}
        resp = client.post("/sentences", json=sentence_data)
        assert resp.status_code == status.HTTP_201_CREATED

        resp_obj = sencente_schema.SentenceCreateResponse(**resp.json())
        assert resp_obj.sentence == "hello, world"
        assert resp_obj.translation == "こんにちは、せかい"
        assert resp_obj.counter == 0


class TestPatchSentence:
    def test_patch_sentence(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")

        sentence_json = {"sentence": "updated", "translation": "updated"}
        resp = client.patch(f"/sentences/{sentence.id}", json=sentence_json)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["sentence"] != "hoge"
        assert resp_obj["sentence"] == "updated"
        assert resp_obj["translation"] != "hage"
        assert resp_obj["translation"] == "updated"

    def test_patch_sentence_with_only_sentence(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")

        sentence_json = {"sentence": "updated"}
        resp = client.patch(f"/sentences/{sentence.id}", json=sentence_json)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["sentence"] != "hoge"
        assert resp_obj["sentence"] == "updated"
        assert resp_obj["translation"] == "hage"
        assert resp_obj["translation"] != "updated"

    def test_patch_sentence_with_only_translation(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")

        sentence_json = {"translation": "updated"}
        resp = client.patch(f"/sentences/{sentence.id}", json=sentence_json)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["sentence"] == "hoge"
        assert resp_obj["sentence"] != "updated"
        assert resp_obj["translation"] != "hage"
        assert resp_obj["translation"] == "updated"

    def test_patch_sentence_without_no_params(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")

        sentence_json = {}
        resp = client.patch(f"/sentences/{sentence.id}", json=sentence_json)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_patch_sentence_with_wrong_id(self, client):
        sentence_json = {"sentence": "updated", "translation": "updated"}
        resp = client.patch(f"/sentences/872364", json=sentence_json)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestCountSentence:
    def test_count_sentence(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")
        assert sentence.counter == 0

        resp = client.patch(f"/sentences/{sentence.id}/count")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["counter"] == 1

    def test_count_sentence_with_wrong_id(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")
        assert sentence.counter == 0

        resp = client.patch(f"/sentences/123/count")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteSentence:
    def test_delete_sentence(self, client):
        sentence = SentenceFactory.create_sentence(client, "hoge", "hage")

        resp = client.get("/sentences")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        resp = client.delete(f"/sentences/{sentence.id}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == None

    def test_try_to_delete_sentence_with_wrong_id(self, client):
        resp = client.delete("/sentences/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
