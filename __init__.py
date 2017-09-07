from __future__ import print_function
from flask import Flask #, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os, sys

login_manager = LoginManager()
login_manager.session_protection = 'strong'
#login_manager.login_view = 'auth.login'

#db = SQLAlchemy()
#blueprint = Blueprint('auth', __name__)

#def create_app(config_name):
#    wheels = Flask(__name__)
#    wheels.config.from_object(config[config_name])
#    config[config_name].init_app(wheels)
#
#    #bootstrap.init_app(app)
#    #mail.init_app(app)
#    #moment.init_app(app)
#    db.init_app(wheels)
#    login_manager.init_app(wheels)
#    #pagedown.init_app(app)
#
#    #if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
#    #    from flask_sslify import SSLify
#    #    sslify = SSLify(app)
#
#    from .main import main as main_blueprint
#    app.register_blueprint(main_blueprint)
#
#    from .auth import auth as auth_blueprint
#    app.register_blueprint(auth_blueprint, url_prefix='/auth')
#
#    from .api_1_0 import api as api_1_0_blueprint
#    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
#
#    return app

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'wheels.db')
db_uri = 'sqlite:///{}'.format(db_path)
wheels = Flask(__name__)
wheels.config['SQLALCHEMY_DATABASE_URI'] = db_uri
wheels.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
wheels.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(wheels)
db = SQLAlchemy(wheels)
db.create_all()

from wheels import views