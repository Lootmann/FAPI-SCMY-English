from random import randint, sample
from string import ascii_letters

import pytest
from fastapi import status

from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema
from tests.init_async_client import async_client as client


def random_string(min_: int = 5, max_: int = 20) -> str:
    return "".join(sample(ascii_letters, randint(min_, max_)))


def fixed_string(size=5) -> str:
    return random_string(size, size)


class WordFactory:
    @staticmethod
    async def create_word(client):
        resp = await client.post(
            "/words", json={"spell": fixed_string(), "meaning": fixed_string()}
        )
        return word_schema.WordCreateResponse(**resp.json())
