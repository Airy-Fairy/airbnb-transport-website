# from __future__ import print_function
# import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_paranoid import Paranoid
from flask_bcrypt import Bcrypt
from flask_whooshee import Whooshee
import os

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

app_root = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(app_root, 'wheels.db')
db_uri = 'sqlite:///{}'.format(db_path)
default_avatar_path = os.path.join(app_root, 'static/imgs')
wheels = Flask(__name__)
wheels.config['SQLALCHEMY_DATABASE_URI'] = db_uri
wheels.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
wheels.config['SECRET_KEY'] = '\x19\xd6;\x19\xb3\x04\xc5;;\x13\x86\x12\xf3\x93\xb1\xed\xa8(\xdb\x14\x93I\xad\x85'
wheels.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
wheels.config['WHOOSHEE_DIR'] = os.path.join(app_root, 'tmp/whoosh')
wheels.config['UPLOAD_FOLDER'] = os.path.join(app_root, 'tmp/uploads')
wheels.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# email configuration
wheels.config['MAIL_SERVER'] = 'smtp.yandex.ru'
wheels.config['MAIL_PORT'] = 465
wheels.config['MAIL_USE_SSL'] = True
wheels.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
wheels.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
wheels.config['SECURITY_EMAIL_SENDER'] = os.environ.get('MAIL_USERNAME') + '@yandex.ru'
WHEELS_MAIL_SUBJECT_PREFIX = '[Sharing Wheels]'
WHEELS_MAIL_SENDER = 'Sharing Wheels Admin <' + os.environ.get('MAIL_USERNAME') + '@yandex.ru>'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

wheels.config['SESSION_COOKIE_SECURE'] = True
wheels.config['SESSION_COOKIE_HTTPONLY'] = True

login_manager.init_app(wheels)
db = SQLAlchemy(wheels)
mail = Mail(wheels)
bcrypt = Bcrypt(wheels)
whooshee = Whooshee(wheels)
csrf = CSRFProtect(wheels)
paranoid = Paranoid(wheels) # strong user session protection
paranoid.redirect_view = '/'


from wheels import views
