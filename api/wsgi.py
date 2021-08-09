from App import create_app, db
from flask import send_file
import click
import os
from flask.cli import with_appcontext
# from App.models import Counter

app = create_app()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


# @click.command(name='create_tables')
# @with_appcontext
# def create_tables():
#     db.create_all()
#
#
# @click.command(name='drop_db')
# @with_appcontext
# def drop_db():
#     """Cleans database"""
#     db.drop_all()
#
#
# @click.command(name='create_count')
# @click.argument('value')
# @with_appcontext
# def create_count(value):
#     RevoCounter = Counter(name="RevolutionCounter", count=value)
#     db.session.add(RevoCounter)
#
#     db.session.commit()
#
#
# app.cli.add_command(create_tables)
# app.cli.add_command(drop_db)
# app.cli.add_command(create_count)

# ctx = app.app_context()
# ctx.push()  # start working on database after that command
# # Database manipulations here
# db.create_all()
# # RevoCounter = Counter(name="RevolutionCounter", count=0)
# # db.session.add(RevoCounter)
# # db.session.commit()
# ctx.pop()  # exit from the app

if __name__ == '__main__':
    app.run()
