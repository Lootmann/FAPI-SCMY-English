import random

from fastapi import status

from api.schemas import talks as talk_schema
from tests.factory import HistoryFactory, TalkFactory, random_string
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
        histories = [
            HistoryFactory.create_hisotry(client),
            HistoryFactory.create_hisotry(client),
        ]

        talk_num = [
            random.randint(5, 8),
            random.randint(9, 12),
        ]

        for history, num in zip(histories, talk_num):
            for _ in range(num):
                talk_data = {
                    "sentence": random_string(),
                    "translation": random_string(),
                }
                resp = client.post(f"/histories/{history.id}/talks", json=talk_data)
                assert resp.status_code == status.HTTP_201_CREATED

            # check all history's talk
            resp = client.get(f"/histoires/{history.id}/talks")
            assert resp.status_code == status.HTTP_200_OK
            assert len(resp.json()) == num


class TestPostTalk:
    def test_post_talk(self, client):
        history = HistoryFactory.create_hisotry(client)

        talk_data = {"sentence": "hoge", "translation": "hage"}
        resp = client.post(f"/histories/{history.id}/talks", json=talk_data)
        assert resp.status_code == status.HTTP_201_CREATED

        # check talk
        resp_obj = talk_schema.TalkCreateResponse(**resp.json())
        assert resp_obj.order_id == 1

        # check sentence
        resp = client.get("/sentences")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        # check history
        resp = client.get("/histories")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        # check all history's talk
        resp = client.get(f"/histoires/{history.id}/talks")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

    def test_post_talk_with_wrong_history_id(self, client):
        talk_data = {"sentence": "hoge", "translation": "hage"}
        resp = client.post("/histories/123/talks", json=talk_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_post_talk_factory(self, client):
        history = HistoryFactory.create_hisotry(client)
        sentence = random_string()
        translation = random_string()
        talk_response = TalkFactory.create_talk(
            client, sentence, translation, history.id
        )

        assert talk_response.order_id == 1
        assert talk_response.sentence.sentence == sentence
        assert talk_response.sentence.translation == translation
