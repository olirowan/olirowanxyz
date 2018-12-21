import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENVIRONMENT_TYPE = os.environ.get('ENVIRONMENT_TYPE')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOG_ADMIN_USER = os.environ.get('BLOG_ADMIN_USER')
    BLOG_ADMIN_ID = os.environ.get('BLOG_ADMIN_ID')
    MYSQL_BACKUP_USER = os.environ.get('MYSQL_BACKUP_USER')
    MYSQL_BACKUP_PASS = os.environ.get('MYSQL_BACKUP_PASS')

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    ADMINS = ['admin@olirowan.xyz']

    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    POSTS_PER_PAGE = 5
    SITE_WIDTH = 800
