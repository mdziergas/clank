from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from clankapp.models import add_user, is_valid_signup, is_valid_login
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
        else:
            message = checked_signup['message']
            flash(message, category=checked_signup['category'])
    return render_template('auth/signup.html')

    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        
        username = request.form['username']
        password = request.form['password']
        login_valid = is_valid_login(username, password)
        if login_valid == True:
            session["username"] = username
            session['authenticated'] = True
            flash('Logged in', category='success')
            return redirect(url_for('auth.login'))
            
        else:
            flash('Wrong username or password', category='error')
            session.clear()
            session['authenticated'] = False

    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    session['authenticated'] = False
    
    return redirect(url_for('auth.login'))

