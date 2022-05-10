from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    tracker = db.relationship("Tracker", backref='user', lazy=True)
    log = db.relationship("Logs", backref='user',lazy=True)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'emaild' : self.email
        }


class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    type = db.Column(db.String)
    value_types = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    log = db.relationship("Logs", backref='tracker')

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'type' : self.type,
            'value_types' : self.value_types,
            'description' : self.description
        }


class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.String)
    time_stamp = db.Column(db.Integer)
    note = db.Column(db.String)
    type = db.Column(db.String)

    def serialize(self):
        return {
            'id' : self.id,
            'tracker_id' : self.tracker_id,
            'user_id' : self.user_id,
            'value' : self.value,
            'time_stamp' : self.time_stamp,
            'note' : self.note,
            'type' : self.type
        }
