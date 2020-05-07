from mongoengine import StringField, ListField, ReferenceField, EmailField, PULL, CASCADE
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Job(db.Document):
    company = StringField(required=True)
    position = StringField(required=True)
    status = StringField(required=True)
    notes = StringField(required=True)
    resume = StringField(required=False)
    cover_letter = StringField(required=False)
    added_by = ReferenceField('User')

class User(db.Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    jobs = ListField(ReferenceField('Job', reverse_delete_rule=PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Job, 'added_by', CASCADE)