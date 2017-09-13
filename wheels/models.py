from __future__ import print_function
from flask_login import UserMixin
from wheels import wheels, db
import flask_whooshalchemy as wa
from werkzeug.security import generate_password_hash, \
	 check_password_hash
import sys

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	phone = db.Column(db.String(32), index=True)
	name = db.Column(db.String(64))
	surname = db.Column(db.String(64))
	reg_date = db.Column(db.Date)
	bday = db.Column(db.Date)
	password_hash = db.Column(db.String(128))
	avatar = db.Column(db.String(32))
	vehicles = db.relationship('Vehicle', backref='owner', lazy='dynamic')
	#confirmed = db.Column(db.Boolean, default=False)

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

	def get_rating(self):
		rate = 0.0
		vehicles = self.vehicles.all()
		if vehicles != []:
			for vehicle in vehicles:
				rate += vehicle.rating
			rate /= float(len(vehicles))
		return int(round(rate))

	def get_reviews_count(self):
		reviews = 0
		vehicles = self.vehicles.all()
		if vehicles != []:
			for vehicle in vehicles:
				reviews += vehicle.review_count
		return reviews

class Vehicle(db.Model):
	__tablename__ = 'vehicles'
	__searchable__ = ['show_name', 'description']
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(16))
	model = db.Column(db.String(16))
	year = db.Column(db.Integer)
	show_name = db.Column(db.String(64))
	price = db.Column(db.Integer)
# are we need it?
	rating = db.Column(db.Float)
	review_count = db.Column(db.Integer)
# end
	description = db.Column(db.String(256))
	photo = db.Column(db.String(32))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	reviews = db.relationship('Review', backref='target', lazy='dynamic')

class Review(db.Model):
	__tablename__ = 'reviews'
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer)
	text = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime)
	uid = db.Column(db.Integer, db.ForeignKey('users.id'))
	ownid = db.Column(db.Integer, db.ForeignKey('users.id'))
	vid = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

wa.whoosh_index(wheels, Vehicle)

def db_whoosh():
	wa.whoosh_index(wheels, Vehicle)