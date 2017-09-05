from flask import render_template, redirect, url_for, request
from wheels import wheels

@wheels.route('/')
def root():
	return render_template('index.html')

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
		email = request.form['email']
		password = request.form['password']
		return render_template('pages/templates/signin.html')