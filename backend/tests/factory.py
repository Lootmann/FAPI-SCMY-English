from random import randint, sample
from string import ascii_letters

from api.schemas import histories as history_schema
from api.schemas import sentences as sentence_schema
from api.schemas import talks as talk_schema
from api.schemas import words as word_schema
from tests.init_client import client


def random_string(min_: int = 5, max_: int = 20) -> str:
    return "".join(sample(ascii_letters, randint(min_, max_)))


class WordFactory:
    @staticmethod
    def create_word(client, spell: str, meaning: str):
        resp = client.post("/words", json={"spell": spell, "meaning": meaning})
        return word_schema.WordCreateResponse(**resp.json())


class SentenceFactory:
    @staticmethod
    def create_sentence(client, sentence: str, translation: str):
        resp = client.post(
            "/sentences",
            json={
                "sentence": sentence,
                "translation": translation,
            },
        )
        return sentence_schema.SentenceCreateResponse(**resp.json())


class HistoryFactory:
    @staticmethod
    def create_hisotry(client):
        resp = client.post("/histories")
        return history_schema.HistoryCreateResponse(**resp.json())


class TalkFactory:
    @staticmethod
    def create_talk(client, sentence: str, translation: str, history_id: int):
        talk_body = {"sentence": sentence, "translation": translation}
        resp = client.post(f"/histories/{history_id}/talks", json=talk_body)
        return talk_schema.TalkCreateResponse(**resp.json())
