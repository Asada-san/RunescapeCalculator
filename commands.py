import click
from flask.cli import with_appcontext

from App import create_app, db
from App.models import Counter


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
