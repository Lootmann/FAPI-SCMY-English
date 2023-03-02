from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel
from api.schemas import sentences as sentence_schema


def test_sentence_model_repr():
    sentence_body = sentence_schema.Sentence(
        id=1, sentence="Hello World", translation="こんにちは、せかい"
    )
    sentence = SentenceModel(**sentence_body.dict())
    sentence.counter = 0

    assert (
        str(sentence)
        == f"<Sentence (id, sent, trans, counter, talk) = (1, Hello World, こんにちは、せかい, 0, None)>"
    )


def test_sentence_model_repr_with_talk():
    sentence = SentenceModel(id=1, sentence="hello", translation="Bonjour", counter=0)
    talk = TalkModel(id=1, order_id=1, sentence=sentence)
    sentence.talk = talk

    talk = "<Talk (id, order, sentence) = (1, 1, hello)>"
    assert (
        str(sentence)
        == f"<Sentence (id, sent, trans, counter, talk) = (1, hello, Bonjour, 0, {talk})>"
    )
