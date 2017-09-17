from flask import current_app
from flask_login import UserMixin
from wheels import wheels, db, whooshee
from flask_whooshee import Whooshee
from werkzeug.security import generate_password_hash, \
	 check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	guid = db.Column(db.String(32), unique=True)
	email = db.Column(db.String(64), unique=True, index=True)
	phone = db.Column(db.String(32), index=True)
	name = db.Column(db.String(64))
	surname = db.Column(db.String(64))
	reg_date = db.Column(db.Date)
	bday = db.Column(db.Date)
	password_hash = db.Column(db.String(128))
	avatar = db.Column(db.String(32))
	confirmed = db.Column(db.Boolean, default=False)
	about_me = db.Column(db.String(256))
	vehicles = db.relationship('Vehicle', backref='owner', lazy='dynamic')

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password, method='pbkdf2:sha512', salt_length=32)

	def verify_password(self, candidate):
		return check_password_hash(self.password_hash, candidate)

	def generate_confirmation_token(self, expiration=3600):
		ser = Serializer(current_app.config['SECRET_KEY'], expiration)
		return ser.dumps({'confirm': self.id})

	def confirm(self, token):
		ser = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = ser.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, new_password):
		self.password = new_password
		db.session.add(self)

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

class Review(db.Model):
	__tablename__ = 'reviews'
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer)
	text = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime)
	uid = db.Column(db.Integer, db.ForeignKey('users.id'))
	ownid = db.Column(db.Integer, db.ForeignKey('users.id'))
	vid = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

@whooshee.register_model('show_name', 'description')
class Vehicle(db.Model):
	__tablename__ = 'vehicles'
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(16))
	model = db.Column(db.String(16))
	year = db.Column(db.Integer)
	show_name = db.Column(db.String(64))
	price = db.Column(db.Integer)
	rating = db.Column(db.Float)
	review_count = db.Column(db.Integer)
	description = db.Column(db.String(256))
	photo = db.Column(db.String(32))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	reviews = db.relationship('Review', backref='target', lazy='dynamic')
