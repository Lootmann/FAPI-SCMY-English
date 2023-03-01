from random import randint, sample
from string import ascii_letters

from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema
from tests.init_async_client import async_client as client


def random_string(min_: int = 5, max_: int = 20) -> str:
    return "".join(sample(ascii_letters, randint(min_, max_)))


class WordFactory:
    @staticmethod
    async def create_word(
        client,
        spell: str,
        meaning: str,
    ):
        resp = await client.post("/words", json={"spell": spell, "meaning": meaning})
        return word_schema.WordCreateResponse(**resp.json())


class SentenceFactory:
    @staticmethod
    async def create_sentence(client, sentence: str, translation: str):
        resp = await client.post(
            "/sentences",
            json={
                "sentence": sentence,
                "translation": translation,
            },
        )
        return sentence_schema.SentenceCreateResponse(**resp.json())
