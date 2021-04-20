from flask import current_app, abort
from App import db


class Counter(db.Model):
    """
    The Count object.

    count:      Total amount of simulations.    :type int
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)



# class Dashboard(db.Model):
#     """
#     The Dashboard object.
#
#     count:          Number of dashboards at the moment of creation.     :type int
#     id:             Unique generated id.                                :type int
#     title:          Title of the dashboard.                             :type str
#     content:        Content of the dashboard.                           :type json
#     tags:           Tags of the dashboard.                              :type json
#     private:        True if the dashboard is for private use only.      :type boolean
#     created_on:     Creation date.                                      :type datetime
#     user_id:        The id of the creator (user).                       :type str
#     leeches:        Current users using the dashboard.                  :type object
#     """
#
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