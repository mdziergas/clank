from flask import Blueprint, render_template, request, flash, session
from ultimateflasktemplate.models import add_user, is_valid_signup, is_valid_login
import json

auth = Blueprint('auth', __name__, template_folder='templates',static_folder='static', url_prefix='/')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        checked_signup = is_valid_signup(email, username, password, password2)
        
        if checked_signup['category'] == 'success': # should probably change to a boolean
            add_user(username, email, password)
            flash('Account created', category='success')
            session['auth'] = 'signup succeeded'
        else:
            message = checked_signup['message']
            flash(message, category=checked_signup['category'])
            session['auth'] = 'signup failed'
    return render_template('signup.html')

    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        login_valid = is_valid_login(username, password)
        if login_valid == True:
            flash('Logged in', category='success')
            session['authenticated'] = True
            return f"{username}"
            
        else:
            flash('Wrong username or password', category='error')
            session['authenticated'] = False

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session['authenticated'] = False
    return "logged out"

