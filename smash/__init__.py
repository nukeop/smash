from flask import Flask
from . import config, database, log, models


log.configure_logging()
app = Flask(__name__)
conf = config.Config('config.json')
conf.save()
db = database.Database(conf.config["DBNAME"])
models.init_models(db)


from . import views
