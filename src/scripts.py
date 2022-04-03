import click
from dotenv import load_dotenv

load_dotenv()


def dev():
    from uvicorn import run

    run("app:app", reload=True, reload_dirs="app")


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
