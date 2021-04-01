from flask import Flask, session
from .home.views import home
from .auth.views import auth
from .recipes.views import recipes
import os

app = Flask(__name__)
app.config.from_object('config')
#app.config.from_pyfile('config.py')
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(recipes, url_prefix='/')

app.secret_key = os.environ.get("SECRET_KEY")
