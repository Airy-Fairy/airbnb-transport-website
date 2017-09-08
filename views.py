from __future__ import print_function
from wheels import wheels, login_manager, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, \
						login_required, current_user
from models import User

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

@wheels.route('/help')
def help():
	return render_template('pages/help.html', title='Help')

@wheels.route('/terms_of_use')
def terms_of_use():
	return render_template('pages/terms.html', title='Terms of Use')

@wheels.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(email=request.form['email']).first()
		if user is not None and user.verify_password(request.form['password']):
			#print('i\'m here!', file=sys.stderr)
			# for remember_me checkbox
			#print(request.form.get('remember'), file=sys.stderr)
			login_user(user, False)
			return redirect(request.args.get('next') or url_for('index'))
		flash('Invalid email or password.')
	return redirect(url_for('index'))

@wheels.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))

@wheels.route('/sign-up', methods=['GET','POST'])
def sign_up():
	print('i\'m here!', file=sys.stderr)
	if request.method == 'POST':
		print(request.form['email'], file=sys.stderr)
		print(request.form['phone'], file=sys.stderr)
		print(request.form['name'], file=sys.stderr)
		print(request.form['surname'], file=sys.stderr)
		print(request.form['password'], file=sys.stderr)

		user = User(email=request.form['email'],
					phone=request.form['phone'],
					first_name=request.form['name'],
					last_name=request.form['surname'],
					password=request.form['password'])
		db.session.add(user)
		db.session.commit()
		#token = user.generate_confirmation_token()
		#send_email
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('index'))
	flash('Something has gone wrong :(')
	return redirect(url_for('index'))