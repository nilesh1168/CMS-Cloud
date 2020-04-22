from flask import Flask
from flask_bootstrap import Bootstrap
from POC.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jsglue import JSGlue

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login.login_view = 'login'
jsglue = JSGlue(app)
import POC.routes, POC.models