from .database import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    tracker_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    track_type = db.Column(db.String, nullable=False)
    settings = db.Column(db.String)

class TrackerLog(db.Model):
    __tablename__ = 'tracker_log'
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.tracker_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String)

