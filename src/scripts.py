import click
from dotenv import load_dotenv

load_dotenv()


@click.group()
def server():
    pass


@server.command()
def dev():
    from uvicorn import run

    run("src.asgi:app", reload=True, reload_dirs="src")


@server.command()
def prod():
    from subprocess import run

    run("gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.asgi:app".split(" "))


@click.group()
@click.pass_context
def db(ctx: click.Context):
    from pathlib import Path

    from alembic.config import Config

    alembic_cfg_path = str(Path.cwd() / "alembic.ini")
    alembic_cfg = Config(alembic_cfg_path)

    ctx.ensure_object(dict)
    ctx.obj["alembic_cfg"] = alembic_cfg


@db.command()
@click.option("--message", "-m", type=str, help="Revision message", required=True)
@click.pass_context
def migrate(ctx: click.Context, message: str):
    from alembic import command

    alembic_cfg = ctx.obj["alembic_cfg"]

    command.revision(alembic_cfg, message=message, autogenerate=True)


@db.command()
@click.pass_context
def upgrade(ctx: click.Context):
    from alembic import command

    alembic_cfg = ctx.obj["alembic_cfg"]

    command.upgrade(alembic_cfg, "head")
