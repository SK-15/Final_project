from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    tracker = db.relationship("Tracker", backref='user', lazy=True)
    log = db.relationship("Logs", backref='user',lazy=True)
class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    type = db.Column(db.String)
    value_types = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    log = db.relationship("Logs", backref='tracker')

class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.String, unique=True)
    time_stamp = db.Column(db.Integer)
    note = db.Column(db.String)
