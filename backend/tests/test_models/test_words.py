from api.models import words as WordModel
from api.models.words import Word as WordModel
from api.schemas import words as word_schema


def test_word_model_repr():
    word_body = word_schema.Word(id=1, spell="hello", meaning="こんにちは")
    word = WordModel(**word_body.dict())

    assert str(word) == f"<Word (id, spell, mean) = (1, hello, こんにちは)>"
