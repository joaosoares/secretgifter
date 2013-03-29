import os
basedir = os.path.abspath(os.path.dirname(__file__))

# For forms
CSRF_ENABLED = True
SECRET_KEY = 'Knowledge Bowl'

#For database
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# For Email
MAIL_SERVER = 'smtp.google.com'
