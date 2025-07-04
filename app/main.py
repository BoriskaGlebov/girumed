from contextlib import asynccontextmanager
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.config import logger
from app.exceptions.exceptions_methods import (
    http_exception_handler,
    integrity_error_exception_handler,
    validation_exception_handler,
)

# from app.medias.dao import MediaDAO
# from app.medias.router import router as router_medias
# from app.tweets.dao import LikeDAO, TweetDAO, TweetMediaDAO
# from app.tweets.router import router as router_tweets
# from app.users.dao import FollowDAO, UserDAO
# from app.users.router import router as router_users
# from migrations_script import run_alembic_command

# API теги и их описание
tags_metadata: List[Dict[str, Any]] = [
    {
        "name": "users",
        "description": "Получаются данные по пользователям",
    },
    {
        "name": "tweets",
        "description": "Операции с Твитами",
        "externalDocs": {
            "description": "Ссылка на документацию",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {"name": "medias", "description": "Работа с медиафайлами"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Действия перед запуском приложения.

    :param app:
    :return:
    """
    logger.info("Перед первым запуском необходимо убедиться в актуальности версии миграции")
    # if os.path.split(os.getcwd())[1] == "app":
    #     run_alembic_command("cd ..; alembic upgrade head;alembic current")
    # elif os.path.split(os.getcwd())[1] == "kill_twitter":
    #     run_alembic_command("alembic upgrade head;alembic current")
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # async for session in get_session():
    #     await UserDAO.add(session, **{"first_name": "Test_name", "last_name": "Test_surname", "api_key": "test"})
    #     [await UserDAO.add(session, **user.to_dict()) for user in generate_users(100)]
    #     [await FollowDAO.add(session, **follow.to_dict()) for follow in generate_follow(100)]
    #     [await MediaDAO.add(session, **MediaFactory().to_dict()) for _ in range(1, 21)]
    #     [await TweetDAO.add(session, **TweetFactory().to_dict()) for _ in range(100)]
    #     [await LikeDAO.add(session, **like.to_dict()) for like in generate_likes(100)]
    #     [await TweetMediaDAO.add(session, **inst.to_dict()) for inst in generate_tweet_media(100)]
    yield


app = FastAPI(
    debug=True,
    title="Girumed Test API",
    summary="Соберите минимальный, но полноценный микросервис для записи пациентов и "
    "подготовьте его так, чтобы коллега мог развернуть проект за пару "
    "минут и сразу увидеть живой API.",
    description="""
---
# Girumed Test API

## Сервис и бизнес-логика
1. Напишите приложение на FastAPI или Flask.
2. Создайте модель Appointment и два эндпойнта:
3. POST /appointments — создать запись;
4. GET /appointments/{id} — получить запись по ID.
5. В базе должна быть уникальная пара doctor_id + start_time, чтобы один врач не принимал двух пациентов одновременно.


---

""",
    openapi_tags=tags_metadata,
    contact={
        "name": "Boriska Glebov",
        "url": "http://localhost:8000/docs",
        "email": "BorisTheBlade.glebov@yandex.ru",
    },
    lifespan=lifespan,
)

# app.include_router(router_users)
# app.include_router(router_tweets)
# app.include_router(router_medias)

# # для тестовой разработки подключение статических файлов
# app.mount("/static", StaticFiles(directory=settings.static_path()), name="static")
# templates = Jinja2Templates(directory=settings.template_path())

# Определение обработчиков исключений
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(IntegrityError, integrity_error_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]

# @app.get("/", response_class=HTMLResponse)
# async def hello_world(request: Request):
#     """Роут для загрузки самой страницы."""
#     return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
