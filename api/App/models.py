from flask import current_app, abort
from api.App import db
from sqlalchemy.sql import func


class Counter(db.Model):
    """
    The Count object.

    count:      Total amount of simulations.    :type int
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)


class List(db.Model):
    """
    The List object.

    id:             Unique generated id.                                :type int
    title:          Title of the dashboard.                             :type str
    created_on:     Creation date.                                      :type datetime
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    json = db.Column(db.JSON, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())

    #     count = db.Column(db.Integer, primary_key=True)
    #     id = db.Column(db.String(36), nullable=False)
    #     title = db.Column(db.String(30), nullable=False)
    #     content = db.Column(db.PickleType, nullable=False, default=[])
    #     tags = db.Column(db.PickleType, nullable=False, default=[])
    #     private = db.Column(db.Boolean, nullable=False)
    #     created_on = db.Column(db.DateTime, nullable=False)
    #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #     # elements = db.relationship('Event', secondary=elements, backref='hosts', lazy=True)
    #     leeches = db.relationship('User', secondary=leeches, backref='dashboards', lazy=True)
    #
    #     def __repr__(self):
    #         """
    #         __repr__ returns the object representation, now manually changed.
    #         """
    #
    #         return f"Dashboard: '{self.title}'"
