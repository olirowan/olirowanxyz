import os
import logging
from flask import Flask
from config import Config
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

mail = Mail(app)

bootstrap = Bootstrap(app)
moment = Moment(app)


log_path = os.path.join(app.config['WRITE_PATH'], 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

file_handler = RotatingFileHandler(log_path + '/olirowanxyz_app.log', maxBytes=10000000, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.DEBUG)
app.logger.info('STARTED olirowanxyz')

task_schedule = BackgroundScheduler(daemon=True)
task_schedule.start()

from app import routes, models, errors
