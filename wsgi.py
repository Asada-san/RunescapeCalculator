from App import create_app, db
import click
from flask.cli import with_appcontext
from App.models import Counter

app = create_app()


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


app.cli.add_command(create_tables)

# ctx = app.app_context()
# ctx.push()  # start working on database after that command
# # Database manipulations here
# db.create_all()
# # counter = Counter(count=0)
# # db.session.add(counter)
# # db.session.commit()
# ctx.pop()  # exit from the app

if __name__ == '__main__':
    app.run(debug=True)
