import os
from flask import Flask
from . import config, database, log, models


log.configure_logging()
app = Flask(__name__)
conf = config.Config('config.json')

# This flag tells the program it's deployed on heroku
if 'HEROKU' in os.environ:
    conf.add(('HEROKU', 1))

# Load app name from environment if it's not in the config
if ('APPNAME' in conf.config and
    conf.config['APPNAME']=="" and
    'APPNAME' in os.environ):
    conf.add(('APPNAME', os.environ['APPNAME']))

# Load app brand name from environment if it's not in the config
if ('APPBRAND' in conf.config and
    conf.config['APPBRAND']=="" and
    'APPBRAND' in os.environ):
    conf.add(('APPBRAND', os.environ['APPBRAND']))

# Set the secret key
if 'SECRETKEY' in conf.config:
    app.secret_key = conf.config['SECRETKEY']
else:
    exit("Secret key not set.")

db = database.Database(conf.config["DBNAME"])
models.init_models(db)


from . import views
