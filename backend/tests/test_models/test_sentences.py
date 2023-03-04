from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel


def test_sentence_model_repr():
    sentence = SentenceModel(
        id=1, sentence="Hello World", translation="こんにちは、せかい", counter=0
    )

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
