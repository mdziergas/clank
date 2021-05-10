from flask import Blueprint, render_template, session, url_for, redirect, abort, send_from_directory, request
from clankapp.models import db
home = Blueprint('home', __name__, template_folder='templates',static_folder='static', url_prefix='/')
recipes = db['recipes']


@home.route('/')
def startpage():
    top_recipes = db.recipes.find({}).sort("upvotes", -1)
    new_recipes = db.recipes.find({}).sort("date_added", -1)
    
    return render_template('home/home.html', top_recipes = top_recipes, new_recipes = new_recipes)

@home.route('/alcoholic')
def alcoholic():
    top_recipes = db.recipes.find({'category':'Alcoholic'}).sort("upvotes", -1)
    new_recipes = db.recipes.find({'category':'Alcoholic'}).sort("date_added", -1)
    
    return render_template('home/alcoholic.html', top_recipes = top_recipes, new_recipes = new_recipes)

@home.route('/non-alcoholic')
def nonalcoholic():
    top_recipes = db.recipes.find({'category':'Non-alcoholic'}).sort("upvotes", -1)
    new_recipes = db.recipes.find({'category':'Non-alcoholic'}).sort("date_added", -1)
    
    return render_template('home/nonalcoholic.html', top_recipes = top_recipes, new_recipes = new_recipes)


@home.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('home.startpage'))

@home.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_term = form['search_string']
        if (search_term != ''):
            return render_template('home/search.html', all_recipes=recipes.find({'$text':{'$search': search_term}}))
        return render_template('home/search.html', message='Nothing Found')
    return render_template('home/search.html', message='Nothing Found')



@home.errorhandler(404)
def not_found(e):
    return "404", 404



@home.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@home.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')