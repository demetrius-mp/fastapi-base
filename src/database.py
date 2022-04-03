from sqlmodel import create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from src.settings import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url


def engine_factory(database_url: str):
    if database_url.startswith("sqlite"):
        return create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

    return create_engine(SQLALCHEMY_DATABASE_URL)


engine = engine_factory(SQLALCHEMY_DATABASE_URL)

# remove when https://github.com/tiangolo/sqlmodel/issues/189 is closed
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
