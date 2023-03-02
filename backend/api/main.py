from fastapi import FastAPI

from api.routers.histories import router as history_router
from api.routers.sentences import router as sentence_router
from api.routers.talks import router as talk_router
from api.routers.words import router as word_router

app = FastAPI()

app.include_router(sentence_router)
app.include_router(word_router)
app.include_router(history_router)
app.include_router(talk_router)
