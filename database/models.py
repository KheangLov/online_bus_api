from flask_bcrypt import generate_password_hash, check_password_hash
from database.db import db

class Bus(db.Document):
  name = db.StringField(required=True, unique=True)
  description = db.StringField(required=True)
  status = db.StringField(required=True)
  user_id = db.ReferenceField('User')

class User(db.Document):
  name = db.StringField(required=True, unique=True)
  email = db.EmailField(required=True, unique=True)
  password = db.StringField(required=True, min_length=6)
  buses = db.ListField(db.ReferenceField('Bus', reverse_delete_rule=db.PULL))

  def hash_password(self):
    self.password = generate_password_hash(self.password).decode('utf8')

  def check_password(self, password):
    return check_password_hash(self.password, password)

User.register_delete_rule(Bus, 'user_id', db.CASCADE)
