from __future__ import print_function
from wheels import wheels, db, login_manager, \
				   ALLOWED_EXTENSIONS, default_avatar_path
from flask import render_template, redirect, url_for, request, flash, \
				  jsonify, send_from_directory, abort
from flask_login import login_user, logout_user, \
						login_required, current_user
from werkzeug.utils import secure_filename
from models import User, Vehicle, Review, Serializer
from datetime import date, datetime, timedelta
from email import send_email
import json, os, uuid

# tests only
import sys # sys.stderr

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

@wheels.route('/feedback')
def feedback():
	return render_template('help.html', title='Help')

@wheels.route('/terms_of_use')
def terms_of_use():
	return render_template('terms.html', title='Terms of Use')

# Stupid global variables
attempts = {}
threshold = 3
delta = timedelta(seconds=5) # just for tests
# delta = timedelta(minutes=30)

@wheels.route('/login', methods=['POST'])
def login():
	user = User.query.filter_by(email=request.form['email']).first()
	if user is not None:
		# Check attempts
		if request.form['email'] not in attempts:
			attempts[request.form['email']] = {'cnt': 1, 'last': datetime.now()}
		else:
			if attempts[request.form['email']]['cnt'] == threshold:
				if datetime.now() - attempts[request.form['email']]['last'] <= delta:
					return jsonify({'failed': True, 'attempts': False})
				else:
					attempts[request.form['email']] = {'cnt': 1, 'last': datetime.now()}
			else:
				attempts[request.form['email']]['cnt'] += 1
				attempts[request.form['email']]['last'] = datetime.now()
		# Check password
		if user.verify_password(request.form['password']):
			rm = True if request.form.get('remember') == 'on' else False
			login_user(user, rm)
			return jsonify({'failed': False, 'attempts': True})
		else:
			return jsonify({'failed': True, 'attempts': True})

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
			user = User(email=request.form['email'],
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
				os.mkdir(os.path.join(user_directory, 'vehicles'))
			db.session.add(user)
			db.session.commit()
			token = user.generate_confirmation_token()
			send_email(user.email, 'Confirm Your Account',
					   'email/confirm', user=user, token=token)
			flash('A confirmation email has been sent to you by email.')
		else:
			flash('This email is already exists.')
		return redirect(url_for('index'))
	flash('Something has gone wrong :(')
	return redirect(url_for('index'))

@wheels.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('index'))

@wheels.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account',
			   'email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('index'))

@wheels.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('index'))
	return render_template('unconfirmed.html', title='Confirm your account')

@wheels.route('/reset', methods=['POST'])
def password_reset_request():
	if current_user.is_anonymous:
		user = User.query.filter_by(email=request.form['user_email']).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Reset Your Password',
			   'email/reset_password', user=user, token=token)
			flash('An email with instructions to reset your password has been sent to you.')
		flash('This email is unregistered.')
	return redirect(url_for('index', title='Main page'))

@wheels.route('/reset/<token>', methods=['GET','POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	if request.method == 'POST':
		s = Serializer(wheels.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			flash('Your token has been expired or revoked. Try again.')
			return redirect(url_for('index'))
		uid = data.get('reset')
		user = User.query.get_or_404(uid)
		if user is None:
			flash('Password has not been updated.')
			return redirect(url_for('index'))
		user.reset_password(request.form['password'])
		flash('Your password has been updated.')
		return redirect(url_for('index', title='Try to login now.'))
	return render_template('new_password.html', token=token)

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
	search_results = json.dumps(fill_vehicle_array(get_records(query, 4)))
	return render_template('search_results.html', results=search_results)

@wheels.route('/search', methods=['POST'])
def search_more():
	current = int(request.form['current'])
	global all_search_results
	search_results = fill_vehicle_array(get_records(all_search_results, 6, current))
	return jsonify(search_results)

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

def get_records(query, limit, offset=0):
	return query.limit(limit).offset(offset).all()

def get_top_rated_vehicles(current):
	query = Vehicle.query.order_by(Vehicle.rating.desc())
	limit = 3 if not current else 6
	return fill_vehicle_array(get_records(query, limit, current))

@wheels.route('/user')
@login_required
def user_menu():
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	user = current_user.email.split('@')
	return redirect(url_for('user', nickname=user[0], page='settings'))

@wheels.route('/user=<nickname>?<page>', methods=['GET'])
@login_required
def user(nickname, page):
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	page_new = 'user/' + page + '.html'
	if page == 'transport':
		query = Vehicle.query.filter_by(owner=current_user)
		query = query.order_by(Vehicle.id.desc())
		mytransport = fill_vehicle_array(get_records(query, 3))
		return render_template('user/main_page.html',
				nick=nickname, page_new=page_new,
				mytransport=json.dumps(mytransport))
	else:
		return render_template('user/main_page.html',
				nick=nickname, page_new=page_new)

@wheels.route('/user=<nickname>?transport', methods=['POST'])
@login_required
def mytransport_more(nickname):
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	current = request.form['current']
	query = Vehicle.query.filter_by(owner=current_user)
	query = query.order_by(Vehicle.id.desc())
	mytransport = fill_vehicle_array(get_records(query, 3, current))
	return jsonify(mytransport)

@wheels.route('/users/id<uid>')
def user_profile(uid):
	user = User.query.get_or_404(uid)
	if user == None:
		return abort(404)
	rate = user.get_rating()
	reviews_count = user.get_reviews_count()
	review_query = Review.query.filter_by(ownid=user.id).order_by(Review.id.desc())
	reviews = json.dumps(fill_reviews_list(get_records(review_query, 3)))
	vs = Vehicle.query.filter_by(owner=user)
	vehicles = [(v.id, v.show_name) for v in vs]
	return render_template('user/profile_page.html',
							user=user,
							rating=rate,
							reviews_count=reviews_count,
							reviews=reviews,
							vehicles=vehicles)

@wheels.route('/users/id<uid>', methods=['POST'])
def get_more_reviews(uid):
	# returns email or phone on request
	try:
		contact = request.form['contact']
	except:
		pass
	else:
		user = User.query.get_or_404(uid)
		if contact == 'get-phone':
			return user.phone
		else:
			return user.email
	# -----------------------------------
	current = request.form['current']
	review_query = Review.query.filter_by(ownid=uid).order_by(Review.id.desc())
	reviews = fill_reviews_list(get_records(review_query, 3, current))
	return jsonify(reviews)

def fill_reviews_list(reviews):
	retarray = []
	for review in reviews:
		user = User.query.get(review.uid)
		user_name = user.name + ' ' + user.surname
		user_avatar = user.avatar
  		veh_name = Vehicle.query.get_or_404(review.vid).show_name
		# Fixes timestamp from UTC to Moscow
		timestamp = review.timestamp.replace(hour=(review.timestamp.hour + 3) % 24)
		print(review.timestamp, file=sys.stderr)
		retarray.append(\
			{'timestamp':timestamp.strftime('%H:%M:%S %b %d, %Y'), \
			'text':review.text, \
			'rating':review.rating, \
			'vid':review.vid, \
			'uid':review.uid, \
			'veh_name':veh_name, \
			'user_name':user_name, \
			'user_avatar':user_avatar})
	return retarray

@wheels.route('/vehicles/id<vid>')
def vehicle_profile(vid):
	current = Vehicle.query.get_or_404(vid)
	if current == None:
		return abort(404)
	return render_template('transport_info.html',
		vehicle=current,
		rating=int(round(current.rating)))

# returns email or phone on request
@wheels.route('/vehicles/id<vid>', methods=['POST'])
def get_owner_email_phone(vid):
	contact = request.form['contact']
	vehicle = Vehicle.query.get_or_404(vid)
	if contact == 'get-phone':
		return vehicle.owner.phone
	else:
		return vehicle.owner.email

@wheels.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	if 'avatar' not in request.files:
		flash('No file part in request.')
		return redirect(url_for('user_menu'))
	file = request.files['avatar']
	if file and allowed_file(file.filename):
		save_path = wheels.config['UPLOAD_FOLDER'] + '/' + current_user.email
		# remove old avatar
		avatar_path = os.path.join(save_path, current_user.avatar)
		if os.path.exists(avatar_path):
			os.remove(avatar_path)
		# save new avatar
		filename = secure_filename(file.filename)
		file.save(os.path.join(save_path, filename))
		# change db avatar value
		current_user.avatar = filename
		user_name = current_user.email.split('@')[0]
		return redirect(url_for('user', nickname=user_name, page='photo'))
	flash('Sorry, server can\'t upload this file.')
	return redirect(url_for('user_menu'))

@wheels.route('/upload/avatar=<uid>/<filename>')
def upload_user_avatar(uid, filename):
	if filename == 'default':
		return send_from_directory(default_avatar_path, 'default.png')
	user = User.query.get_or_404(uid)
	if user == None:
		return abort(404)
	load_path = os.path.join(wheels.config['UPLOAD_FOLDER'], user.email)
	return send_from_directory(load_path, filename)

@wheels.route('/upload/vehicle=<vid>/<filename>')
def upload_vehicle_photo(vid, filename):
	vehicle = Vehicle.query.get_or_404(vid)
	owner = vehicle.owner
	load_path = os.path.join(wheels.config['UPLOAD_FOLDER'], owner.email)
	load_path = os.path.join(load_path, 'vehicles')
	return send_from_directory(load_path, filename)

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@wheels.route('/add_review', methods=['POST'])
@login_required
def add_review():
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	text = request.form['text_review']
	vid = int(request.form.get('choose_transport'))
	rating = float(request.form['rating'])
	# get vehicle's owner id
	chosen = Vehicle.query.get_or_404(vid)
	owner_id = chosen.owner.id
	# creating new review record
	review = Review.query.filter_by(uid=current_user.id).filter_by(vid=vid).first()
	if review is None:
		review_new = Review(rating=int(rating),
							text=text,
							timestamp=datetime.utcnow(),
							uid=current_user.id,
							ownid=owner_id,
							vid=vid,
							target=chosen)
		db.session.add(review_new)
		# update transport info
		chosen = Vehicle.query.get_or_404(vid)
		chosen.rating = (chosen.rating * chosen.review_count + rating) \
						/ (chosen.review_count + 1)
		chosen.review_count += 1
		db.session.add(chosen)
	else:
		flash('You already rated this vehicle.')
	return redirect(url_for('user_profile', uid=owner_id))

@wheels.route('/add_transport', methods=['POST'])
@login_required
def add_transport():
	if not current_user.confirmed:
		return redirect(url_for('unconfirmed'))
	brand = request.form.get('brand')
	model = request.form.get('model')
	year = 1900 if request.form.get('year') == 'before-1960' else int(request.form.get('year')) + 1960
	price = int(request.form['price'])
	desc = request.form['desc']
	show_name = '{0} {1} ({2})'.format(brand, model, 'before 1960' if year < 1960 else year)
	print (show_name, file=sys.stderr)
	# vehicle photo uploading
	if 'photo' not in request.files:
		flash('No file part in request.')
		return redirect(url_for('user_menu'))
	file = request.files['photo']
	if file and allowed_file(file.filename):
		save_path = wheels.config['UPLOAD_FOLDER'] + '/' + current_user.email + '/vehicles'
		# creating the unique file names for each file
		filename = uuid.uuid4().hex + '.' + file.filename.split('.')[-1]
		file.save(os.path.join(save_path, filename))
		vehicle = Vehicle(brand=brand,
						  model=model,
						  year=year,
						  show_name=show_name,
						  price=price,
						  rating=0.0,
						  review_count=0,
						  description=desc,
						  photo=filename,
						  owner=current_user)
		db.session.add(vehicle)
		db.session.commit()
		user_name = current_user.email.split('@')[0]
		return redirect(url_for('user', nickname=user_name, page='transport'))
	flash('Sorry, server can\'t upload this file.')
	return redirect(url_for('user_menu'))
