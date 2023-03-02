from fastapi import status

from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import talks as talk_schema
from api.schemas import words as word_schema
from tests.factory import HistoryFactory, SentenceFactory, WordFactory, random_string
from tests.init_client import client


class TestGetAllTalks:
    def test_get_all_talks_with_empty(self, client):
        resp = client.get("/talks")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    def test_get_all_talks(self, client):
        pass


class TestGetTalk:
    def test_get_talk(self, client):
        pass


class TestGetAllTalksByHistory:
    def test_get_all_talks_by_history(self, client):
        pass
