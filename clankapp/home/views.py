from flask import Blueprint, render_template, session, url_for, redirect
from clankapp.models import db
home = Blueprint('home', __name__, template_folder='templates',static_folder='static', url_prefix='/')


@home.route('/')
def startpage():
    top_recipes = db.recipes.find({}).sort("upvotes", -1)
    new_recipes = db.recipes.find({}).sort("date_added", -1)
    
    return render_template('home.html', top_recipes = top_recipes, new_recipes = new_recipes)


@home.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('home.startpage'))