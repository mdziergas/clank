from flask import Blueprint, render_template, session, url_for, redirect

home = Blueprint('home', __name__, template_folder='templates',static_folder='static', url_prefix='/')


@home.route('/')
def startpage():
    if "auth" in session:
        print ('auth in session')
        print(session['auth'])
    else:
        print ('auth not in session')
        
    return render_template('home.html')


@home.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('home.startpage'))