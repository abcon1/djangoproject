from app import db
import datetime


class Device(db.Document):
    name = db.StringField(unique=True, required=True)
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    assigned_to = db.IntField(max_value=3)


from werkzeug.security import check_password_hash


class User(db.Document):
    username = db.StringField(required=True, unique=True, min_length=3)
    password = db.StringField(required=True)
    devices = db.ListField()
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password, password)
