"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, redirect, response, template
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

# Registration and authorisation forms
@route('/auth')
@view('auth')
def auth():
    return dict(
        title='Login / Register',
        message='Welcome to the Authorization Page',
        year=datetime.now().year,
        error=None
    )

@route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not username or not password:
        return template('auth', title='Login / Register', message='Welcome to the Authorization Page', 
                        year=datetime.now().year, error='Username and password are required')
    response.set_cookie('username', username, secret='some-secret-key')
    redirect('/home')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not username or not password:
        return template('auth', title='Login / Register', message='Welcome to the Authorization Page', 
                        year=datetime.now().year, error='Username and password are required')
    response.set_cookie('username', username, secret='some-secret-key')
    redirect('/home')

@route('/logout')
def logout():
    response.delete_cookie('username')
    redirect('/auth')