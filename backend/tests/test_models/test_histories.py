from api.models.histories import History as HistoryModel
from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel


def test_history_model_repr_without_talks():
    history = HistoryModel(id=1)
    assert str(history) == "<History (id, talks) = (1, [])>"


def test_history_model_repr():
    sentence = SentenceModel(id=1, sentence="hoge", translation="hige")
    history = HistoryModel(id=1)
    history.talks.append(TalkModel(id=1, order_id=1, sentence=sentence))
    history.talks.append(TalkModel(id=2, order_id=2, sentence=sentence))

    talk1 = "<Talk (id, order, sentence) = (1, 1, hoge)>"
    talk2 = "<Talk (id, order, sentence) = (2, 2, hoge)>"
    assert str(history) == f"<History (id, talks) = (1, [{talk1}, {talk2}])>"
