import click


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
