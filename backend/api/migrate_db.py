from sqlalchemy import create_engine

from api.models.histories import History
from api.models.sentences import Sentence
from api.models.talks import Talk
from api.models.words import Word
from api.settings import Settings

setting = Settings()

engine = create_engine(setting.migrate_db_url, echo=True)


def reset_database():
    Word.metadata.drop_all(bind=engine)
    Word.metadata.create_all(bind=engine)

    Sentence.metadata.drop_all(bind=engine)
    Sentence.metadata.create_all(bind=engine)

    Talk.metadata.drop_all(bind=engine)
    Talk.metadata.create_all(bind=engine)

    History.metadata.drop_all(bind=engine)
    History.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
