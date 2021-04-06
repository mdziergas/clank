from flask import Blueprint, render_template, session, url_for, redirect, request, flash
from clankapp.models import add_recipe, db, upvote
from bson.objectid import ObjectId

recipes = Blueprint('recipes', __name__, template_folder='templates',static_folder='static', url_prefix='/')


@recipes.route('/post-recipe', methods=['GET', 'POST'])
def post_recipe():
    if "authenticated" in session:
        if request.method == 'POST':
            username = session['username']
            recipe_name = request.form['recipe_name']
            category = request.form['category']
            ingredients = request.form['ingredients']
            instructions = request.form['instructions']
            description = request.form['description']
            add_recipe(recipe_name, category, ingredients, instructions, username, description)
            flash("recipe posted", category="success")
    else:
        print ('auth not in session')
        flash("login first", category="danger")
        
    return render_template('post_recipe.html')


@recipes.route('/recipe/<_id>', methods=['GET', 'POST'])
def recipe(_id):
    get_recipe = db.recipes.find_one({'_id':_id})
    username_current = session['username']
    
    if request.method == 'POST': #upvote button
        has_voted = db.users.find_one({'username':username_current})
        last_voted = has_voted.get('upvoted')
        if last_voted:
            pass
        else:
            upvote(_id, None, username_current)
        if session['authenticated'] == True:
            if request.form['upvote'] == 'upvote':
                if has_voted['upvoted'][_id] != 1:
                    print("-"*50)
                    upvote(_id, True, username_current) # true if upvote false if downvote
                    flash("upvoted", category="success")
                else:
                    flash("cant double upvote", category="danger")
            else:
                if has_voted['upvoted'][_id] != -1:
                    upvote(_id, False, username_current) # true if upvote flalse if downvote
                    flash("downvoted", category="danger")
                else:
                    flash("cant double downvote", category="danger")

            get_recipe = db.recipes.find_one({'_id':ObjectId(_id)})
        else: 
            flash("Need to be logged in to vote", category="warning")
        


    return render_template('recipe.html', recipe=get_recipe)

