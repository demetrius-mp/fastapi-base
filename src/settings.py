import os


class Settings:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    sqlalchemy_database_url: str

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
        sqlalchemy_database_url: str,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.sqlalchemy_database_url = sqlalchemy_database_url


def get_settings():
    secret_key = os.environ.get("SECRET_KEY")

    if secret_key is None:
        raise ValueError("[ERROR] You must define a Secret Key")

    algorithm = os.environ.get("ALGORITHM", "HS256")

    access_token_expire_minutes = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    sqlalchemy_database_url = os.environ.get("SQLALCHEMY_DATABASE_URL")

    if not sqlalchemy_database_url:
        raise ValueError("[ERROR] You must define a Database URL")

    return Settings(
        secret_key=secret_key,
        algorithm=algorithm,
        access_token_expire_minutes=int(access_token_expire_minutes),
        sqlalchemy_database_url=sqlalchemy_database_url,
    )


# exported
settings = get_settings()
