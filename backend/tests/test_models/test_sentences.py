from api.models import words as WordModel
from api.models.sentences import Sentence as SentenceModel
from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema


def test_sentence_model_repr():
    sentence_body = sentence_schema.Sentence(
        id=1, sentence="Hello World", translation="こんにちは、せかい"
    )
    sentence = SentenceModel(**sentence_body.dict())
    sentence.counter = 0

    assert (
        str(sentence)
        == f"<Sentence (id, sent, trans, counter) = (1, Hello World, こんにちは、せかい, 0)>"
    )
