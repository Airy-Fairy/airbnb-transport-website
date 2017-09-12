from __future__ import print_function
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os, sys

login_manager = LoginManager()
login_manager.session_protection = 'strong'
#login_manager.login_view = 'auth.login'

app_root = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(app_root, 'wheels.db')
db_uri = 'sqlite:///{}'.format(db_path)
default_avatar_path = os.path.join(app_root, 'static/imgs')
wheels = Flask(__name__)
wheels.config['SQLALCHEMY_DATABASE_URI'] = db_uri
wheels.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
wheels.config['SECRET_KEY'] = '\xd1p\xa4\xe9\xe0\xf3\xb0\xfd\x03\xa4\x0c\xbb\x01\xf4\xf5\x9fJ\x8b\x8d._\xb4Nq\x9e\x0bIa?K?\xfe'
wheels.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
wheels.config['WHOOSH_BASE'] = 'tmp/whoosh'
wheels.config['UPLOAD_FOLDER'] = os.path.join(app_root, 'tmp/uploads')
wheels.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

login_manager.init_app(wheels)
db = SQLAlchemy(wheels)

from wheels import views