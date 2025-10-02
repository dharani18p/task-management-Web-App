from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required

pages_bp = Blueprint('pages_bp', __name__)

# 👇 ADD THIS NEW ROUTE
@pages_bp.route('/')
def index():
    # This redirects the root URL ("/") to the login page URL
    return redirect(url_for('pages_bp.login_page'))


@pages_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@pages_bp.route('/login-page')
def login_page():
    return render_template('login.html')

@pages_bp.route('/tasks-page')
@jwt_required(locations=['cookies'])
def tasks_page():
    return render_template("tasks.html")