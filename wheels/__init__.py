# from __future__ import print_function
# import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

app_root = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(app_root, 'wheels.db')
db_uri = 'sqlite:///{}'.format(db_path)
default_avatar_path = os.path.join(app_root, 'static/imgs')
wheels = Flask(__name__)
wheels.config['SQLALCHEMY_DATABASE_URI'] = db_uri
wheels.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
wheels.config['SECRET_KEY'] = '\xd1p\xa4\xe9\xe0\xf3\xb0\xfd\x03\xa4\x0c\xbb\x01\xf4\xf5\x9fJ\x8b\x8d._\xb4Nq\x9e\x0bIa?K?\xfe'
wheels.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
wheels.config['WHOOSH_BASE'] = 'tmp/whoosh'
wheels.config['UPLOAD_FOLDER'] = os.path.join(app_root, 'tmp/uploads')
wheels.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# email configuration
wheels.config['MAIL_SERVER'] = 'smtp.yandex.ru'
wheels.config['MAIL_PORT'] = 465
wheels.config['MAIL_USE_SSL'] = True
wheels.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
wheels.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
WHEELS_MAIL_SUBJECT_PREFIX = '[Sharing Wheels]'
WHEELS_MAIL_SENDER = 'Sharing Wheels Admin <don.testeroff@yandex.ru>'

login_manager.init_app(wheels)
db = SQLAlchemy(wheels)
mail = Mail(wheels)

from wheels import views
