from app import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
  return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"User('{self.email}')"
    
    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True 

    def is_anonymous(self):
        return False
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8') 
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
