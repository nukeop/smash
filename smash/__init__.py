import os
from flask import Flask
from . import config, database, log, models


log.configure_logging()
app = Flask(__name__)
conf = config.Config('config.json')

# This flag tells the program it's deployed on heroku
if 'HEROKU' in os.environ:
    conf.add(('HEROKU', 1))

db = database.Database(conf.config["DBNAME"])
models.init_models(db)


from . import views
