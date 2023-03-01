from random import randint, sample
from string import ascii_letters

from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema
from tests.init_async_client import async_client as client


def random_string(min_: int = 5, max_: int = 20) -> str:
    return "".join(sample(ascii_letters, randint(min_, max_)))


def fixed_string(size=5) -> str:
    return random_string(size, size)


class WordFactory:
    @staticmethod
    async def create_word(
        client,
        spell: str = fixed_string(),
        meaning: str = fixed_string(),
    ):
        resp = await client.post("/words", json={"spell": spell, "meaning": meaning})
        return word_schema.WordCreateResponse(**resp.json())


class SentenceFactory:
    @staticmethod
    async def create_sentence(client):
        resp = await client.post(
            "/sentences",
            json={
                "sentence": fixed_string(size=10),
                "translation": fixed_string(size=10),
            },
        )
        return sentence_schema.SentenceCreateResponse(**resp.json())
