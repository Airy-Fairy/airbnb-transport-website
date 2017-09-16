import sys
import json
from random import uniform, randint
from datetime import datetime, date
from wheels import db
from wheels.models import User, Vehicle, Review, db_whoosh

def init_user_db():
	db.drop_all()
	db_whoosh()
	db.create_all()
	admin = User(email='glebignatieff@gmail.com',
					 phone='333-333-3333',
					 name='Gleb',
					 surname='Ignatiev',
					 password='pass123',
					 avatar='admin.png',
					 reg_date=datetime.utcnow(),
					 bday=date(1995, 03, 31),
					 confirmed=True)
	db.session.add(admin)
	db.session.commit()
	users = User.query.all()
	print ('Email: {0}').format(users[0].email)

	with open('vehicle_base.json') as f:
		cars = json.load(f)
		i = 1
		for car in cars:
			show_name = '{0} {1} ({2})'.format(car['brand'], car['model'], 'before 1960' if car['year'] < 1960 else car['year'])
			v = Vehicle(brand=car['brand'],
						model=car['model'],
						year=car['year'],
						show_name=show_name,
						price=car['price'],
						rating=uniform(1.0, 5.0),
						review_count=randint(1, 30),
						description=car['description'],
						photo=str(i) + '.jpg', #car['show_name'].replace(' ', '_') + '.jpg',
						owner=admin)
			i += 1
			print v.show_name, v.price, v.rating
			db.session.add(v)
		db.session.commit()

	the_review = Review(rating=1,
						text='sample review',
						timestamp=datetime.utcnow(),
						uid=1, ownid=1, vid=1)
	db.session.add(the_review)
	db.session.commit()
	db.session.delete(the_review)
	db.session.commit()

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == 'init':
			init_user_db()
	else:
		print 'Usage: flask/bin/python database.py init'