from flask import Flask, session, render_template
from .views.home import home
from .views.auth import auth
from .views.recipes import recipes
import os

app = Flask(__name__)
app.config.from_object('config')
#app.config.from_pyfile('config.py')
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(recipes, url_prefix='/')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

app.secret_key = os.environ.get("SECRET_KEY")
