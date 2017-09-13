from __future__ import print_function
from wheels import wheels, login_manager, db, \
				   ALLOWED_EXTENSIONS, default_avatar_path
from flask import render_template, redirect, url_for, request, flash, \
				  jsonify, send_from_directory, abort
from flask_login import login_user, logout_user, \
						login_required, current_user
from werkzeug.utils import secure_filename
from models import User, Vehicle
from datetime import date, datetime
import json, os

# tests only
import sys

all_search_results = None

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@wheels.route('/')
def root():
	return redirect(url_for('index'))

@wheels.route('/index')
def index():
	vehicles = get_top_rated_vehicles(3)
	for vehicle in vehicles:
		url_for('upload_vehicle_photo', vid=vehicle['id'], filename=vehicle['photo'])
	return render_template('index.html', title='Home')

@wheels.route('/index', methods=['POST'])
def index_car_review():
	current = int(request.form['current'])
	if current != None:
		vehicles = get_top_rated_vehicles(current)
		for vehicle in vehicles:
			url_for('upload_vehicle_photo', vid=vehicle['id'], filename=vehicle['photo'])
		return jsonify(vehicles)

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
			bday = date(int(request.form.get('bd_year')) + 1900,  \
						int(request.form.get('bd_month')) + 1, \
						int(request.form.get('bd_day')) + 1)
			user_new = User(email=request.form['email'],
							phone=request.form['phone'],
							name=request.form['name'],
							surname=request.form['surname'],
							bday=bday,
							password=request.form['password'],
							avatar='default',
							reg_date=datetime.utcnow())
			user_directory = os.path.join(wheels.config['UPLOAD_FOLDER'], request.form['email'])
			if not os.path.exists(user_directory):
				os.mkdir(user_directory)
			db.session.add(user_new)
			db.session.commit()
			flash('A confirmation email has been sent to you by email.')
		else:
			flash('This email is already registered.')
		return redirect(url_for('index'))
	flash('Something has gone wrong :(')
	return redirect(url_for('index'))

@wheels.route('/search', methods=['GET'])
def search():
	global all_search_results
	# advanced search
	# GET request
	brand = request.args.get('brand')
	model = request.args.get('model')
	year_from = request.args.get('year_from')
	year_to = request.args.get('year_to')
	price_from = request.args.get('price_from')
	price_to = request.args.get('price_to')
	search_str = request.args.get('search')
	# query filters
	query = Vehicle.query
	if not (brand == model == year_from == year_to == \
			price_from == price_to == search_str == ''):
		query = query.whoosh_search(search_str)
		if brand:
			query = query.filter_by(brand=brand)
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
	all_search_results = query
	search_results = json.dumps(get_vehicles_records(query, 4, 0))
	return render_template('search_results.html', results=search_results)

@wheels.route('/search', methods=['POST'])
def search_more():
	current = int(request.form['current'])
	global all_search_results
	search_results = jsonify(get_vehicles_records(all_search_results, 6, current))
	return search_results

def fill_vehicle_array(vehicles):
	retarray = []
	for vehicle in vehicles:
		retarray.append(\
			{'id':vehicle.id,
			'show_name':vehicle.show_name, \
			'price':vehicle.price, \
			'rating':vehicle.rating, \
			'desc':vehicle.description, \
			'reviews':vehicle.review_count, \
			'photo':vehicle.photo,
			'owner':vehicle.owner.email})
	return retarray

def get_vehicles_records(query, limit, offset=0):
	vehicles = query.limit(limit).offset(offset).all()
	results = fill_vehicle_array(vehicles)
	return results

def get_top_rated_vehicles(current):
	query = Vehicle.query.order_by(Vehicle.rating.desc())
	limit = 3 if not current else 6
	return get_vehicles_records(query, limit, current)

@wheels.route('/user')
@login_required
def user_menu():
	user = current_user.email.split('@')
	return redirect(url_for('user', nickname=user[0], page='settings'))

@wheels.route('/user=<nickname>?<page>')
@login_required
def user(nickname, page):
	page_new = 'user/' + page + '.html'
	if page == 'transport':
		query = Vehicle.query.filter_by(owner=current_user)
		query = query.order_by(Vehicle.id.desc())
		mytransport = get_vehicles_records(query, 3, 0)
		return render_template('user/main_page.html',
				nick=nickname, page_new=page_new,
				mytransport=json.dumps(mytransport))
	else:
		return render_template('user/main_page.html',
				nick=nickname, page_new=page_new)

@wheels.route('/user=<nickname>?transport', methods=['POST'])
@login_required
def mytransport_more():
	return 'nothing to say to you'

@wheels.route('/users/id<id>')
def user_profile(id):
	user = User.query.filter_by(id=id).first()
	if user == None:
		return abort(404)
	rate = get_user_rating(user)
	reviews = get_user_reviews(user)
	vs = Vehicle.query.filter_by(owner=user)
	vehicles = [(v.id, v.show_name) for v in vs]
	print (vehicles, file=sys.stderr)
	return render_template('user/profile_page.html',
							user=user,
							rating=rate,
							reviews=reviews,
							vehicles=vehicles)

def get_user_rating(user):
	vehicles = Vehicle.query.filter_by(owner=user).all()
	rate = 0.0
	if vehicles != []:
		for vehicle in vehicles:
			rate += vehicle.rating
		rate /= float(len(vehicles))
	return int(round(rate))

def get_user_reviews(user):
	vehicles = Vehicle.query.filter_by(owner=user).all()
	reviews = 0
	if vehicles != []:
		for vehicle in vehicles:
			reviews += vehicle.review_count
	return reviews

@wheels.route('/vehicles/id<vid>')
def vehicle_profile(vid):
	current = Vehicle.query.filter_by(id=vid).first()
	if current == None:
		return abort(404)
	return render_template('transport_info.html',
		vehicle=current,
		rating=int(round(current.rating)))

@wheels.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
	if 'avatar' not in request.files:
		flash('No file part in request.')
		return redirect(url_for('user_page'))
	file = request.files['avatar']
	if file.filename == '':
		flash('Please select any file again.')
		return redirect(url_for('user_page'))
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		user_name = current_user.email.split('@')[0]
		save_path = wheels.config['UPLOAD_FOLDER'] + '/' + current_user.email
		file.save(os.path.join(save_path, filename))
		# remove old avatar
		avatar_path = os.path.join(save_path, current_user.avatar)
		if os.path.exists(avatar_path):
			os.remove(avatar_path)
		# change db avatar value
		current_user.avatar = filename
		db.session.commit()
		return redirect(url_for('user', nickname=user_name, page='photo'))
	flash('Sorry, server can\'t upload this file.')
	return redirect(url_for('user_page'))

@wheels.route('/upload/avatar=<uid>/<filename>')
@login_required
def upload_user_avatar(uid, filename):
	#print (filename, file=sys.stderr)
	if filename != 'default':
		user = User.query.filter_by(id=uid).first()
		if user == None:
			return abort(404)
		load_path = os.path.join(wheels.config['UPLOAD_FOLDER'], user.email)
		return send_from_directory(load_path, filename)
	return send_from_directory(default_avatar_path, 'default.png')

@wheels.route('/upload/vehicle=<vid>/<filename>')
def upload_vehicle_photo(vid, filename):
	vehicle = Vehicle.query.filter_by(id=vid).first()
	owner = vehicle.owner
	load_path = os.path.join(wheels.config['UPLOAD_FOLDER'], owner.email)
	load_path = os.path.join(load_path, 'vehicles')
	return send_from_directory(load_path, filename)

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@wheels.route('/create_transport', methods=['POST'])
def create_transport(filename):
	return 'nothing to say to you'