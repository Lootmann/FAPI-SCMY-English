from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel


def test_talk_model_repr():
    sentence = SentenceModel(id=1, sentence="hoge", translation="hige", counter=0)
    talk = TalkModel(id=1, order_id=1, sentence=sentence)
    assert str(talk) == f"<Talk (id, order, sentence) = (1, 1, hoge)>"
