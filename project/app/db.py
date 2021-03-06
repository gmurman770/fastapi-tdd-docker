import logging
import os
import ssl

from fastapi import FastAPI
from pydantic import AnyUrl, BaseModel
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")


class DB(BaseModel):
    """Just for URL parsing."""

    url: AnyUrl


db = DB(url=os.environ.get("DATABASE_URL"))
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
config = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": db.url.host,
                "port": db.url.port,
                "user": db.url.user,
                "password": db.url.password,
                "database": db.url.path.lstrip("/"),
                "ssl": ctx,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.models.tortoise"],
            "default_connection": "default",
        },
    },
}
config2 = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": db.url.host,
                "port": db.url.port,
                "user": db.url.user,
                "password": db.url.password,
                "database": db.url.path.lstrip("/"),
                "ssl": ctx,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["models.tortoise"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(app, config=config)
    # register_tortoise(
    #     app,
    #     db_url=os.environ.get("DATABASE_URL"),
    #     modules={"models": ["app.models.tortoise"]},
    #     generate_schemas=False,
    #     add_exception_handlers=True,
    # )


# new
async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        config=config2
        # db_url=os.environ.get("DATABASE_URL"),
        # modules={'models': ['models.tortoise']},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


# new
if __name__ == "__main__":
    run_async(generate_schema())
