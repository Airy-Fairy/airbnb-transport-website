from flask_login import UserMixin
from wheels import db
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    #vehicles = db.relationship('Vehicle', backref='owner', lazy='dynamic')
    #confirmed = db.Column(db.Boolean, default=False)
    #remember_me = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #def generate_confirmation_token(self, expiration=3600):
    #    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #    return s.dumps({'confirm': self.id})

    #def confirm(self, token):
    #    s = Serializer(current_app.config['SECRET_KEY'])
    #    try:
    #        data = s.loads(token)
    #    except:
    #        return False
    #    if data.get('confirm') != self.id:
    #        return False
    #    self.confirmed = True
    #    db.session.add(self)
    #    return True

    #def generate_reset_token(self, expiration=3600):
    #    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #    return s.dumps({'reset': self.id})

    #def reset_password(self, token, new_password):
    #    s = Serializer(current_app.config['SECRET_KEY'])
    #    try:
    #        data = s.loads(token)
    #    except:
    #        return False
    #    if data.get('reset') != self.id:
    #        return False
    #    self.password = new_password
    #    db.session.add(self)
    #    return True

    #def generate_auth_token(self, expiration):
    #    s = Serializer(current_app.config['SECRET_KEY'],
    #                   expires_in=expiration)
    #    return s.dumps({'id': self.id}).decode('ascii')

class Vehicle():
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(16), index=True)
    model = db.Column(db.String(16), index=True)
    year = db.Column(db.Integer, index=True)
    show_name = db.Column(db.String(64), index=True)    
    price = db.Column(db.Integer, index=True)
    rating = db.Column(db.Float, index=True)
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))