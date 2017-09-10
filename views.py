from __future__ import print_function
from wheels import wheels, login_manager, db
from flask import render_template, redirect, url_for, request, flash, \
				  jsonify
from flask_login import login_user, logout_user, \
						login_required, current_user
from models import User, Vehicle
from datetime import date

# tests only
import sys

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@wheels.route('/')
def root():
	return render_template('index.html', title='Home')

@wheels.route('/index')
def index():
	return render_template('index.html', title='Home')

@wheels.route('/index', methods=['POST'])
def index_car_review():
	current = int(request.form['current'])
	cars = get_cars(current)
	if cars != []:
		return jsonify(cars)
	else:
		flash('End of database.')
		return jsonify(flag='end')
		#return render_template('index.html', title='Home')

@wheels.route('/help')
def help():
	return render_template('help.html', title='Help')

@wheels.route('/terms_of_use')
def terms_of_use():
	return render_template('terms.html', title='Terms of Use')

@wheels.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(email=request.form['email']).first()
		if user is not None and user.verify_password(request.form['password']):
			rm = True if request.form.get('remember') == 'on' else False
			login_user(user, rm)
			return redirect(request.args.get('next') or url_for('index'))
		flash('Invalid email or password.')
	return redirect(url_for('index'))

@wheels.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))

@wheels.route('/sign_up', methods=['GET','POST'])
def sign_up():
	if request.method == 'POST':
		user = User.query.filter_by(email=request.form['email']).first()
		if user is None:
			bday = date(int(request.form.get('bd_year')),  \
					    int(request.form.get('bd_month')) + 1, \
						int(request.form.get('bd_day')) + 1)

			user_new = User(email=request.form['email'],
						phone=request.form['phone'],
						name=request.form['name'],
						surname=request.form['surname'],
						bday=bday,
						password=request.form['password'])
			db.session.add(user_new)
			db.session.commit()
			flash('A confirmation email has been sent to you by email.')
		else:
			flash('This email is already registered.')
		#token = user.generate_confirmation_token()
		#send_email
		
		return redirect(url_for('index'))
	flash('Something has gone wrong :(')
	return redirect(url_for('index'))

#@app.before_request
@wheels.route('/search', methods=['POST'])
def search():
	query = Vehicle.query.whoosh_search(request.form.get('search'))
	#return redirect(url_for('search_results', query=request.form.get('search')))
	
	# advanced search
	# GET request
	#brand = request.args.get('brand')
	#model = request.args.get('model')
	#year_from = request.args.get('year_from')
	#year_to = request.args.get('year_to')
	#price_from = request.args.get('price_from')
	#price_to = request.args.get('price_to')
	
	# POST request
	brand = request.form['brand']
	model = request.form['model']
	year_from = request.form['year_from']
	year_to = request.form['year_to']
	price_from = request.form['price_from']
	price_to = request.form['price_to']

	if brand:
		query = query.filter_by(brand=brand)
		# print (results, file=sys.stderr)
	if model:
		query = query.filter_by(model=model)
	if year_from:
		query = query.filter(Vehicle.year >= year_from)
	if year_to:
		query = query.filter(Vehicle.year <= year_to)
	if price_from:
		query = query.filter(Vehicle.price >= price_from)
	if price_to:
		query = query.filter(Vehicle.year >= price_to)
	records = query.all()
	results = []
	if not records:
		flash('Sorry, we have no your type of vehicle')
	else:
		for record in records:
			results.append({'show_name':record.show_name,\
							'price':record.price, \
							'rating':record.rating, \
							'desc':record.description, \
							'reviews':record.review_count})
		print (records[0].show_name, file=sys.stderr)
	return render_template('search_results.html', results=results)

#@wheels.route('/search?<query>')
#def search_results(query):
#    results = Vehicle.query.whoosh_search(query).all()
#    print (results, file=sys.stderr)
#    return render_template('search_results.html',
#        query = query,
#        results = results)


def get_cars(current):
	if current == 0:
		cars = Vehicle.query.order_by(Vehicle.rating.desc()).limit(3).offset(0).all()
	else:
		cars = Vehicle.query.order_by(Vehicle.rating.desc()).limit(6).offset(current).all()
	if cars is None:
		return []
	ret = []
	for car in cars:
		ret.append({'show_name':car.show_name, 'price':car.price, \
					'rating':car.rating, 'desc':car.description, \
					'reviews':car.review_count})
	return ret