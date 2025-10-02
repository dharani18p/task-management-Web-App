from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required # Make sure this import is at the top

pages_bp = Blueprint('pages_bp', __name__)

@pages_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@pages_bp.route('/login-page')
def login_page():
    return render_template('login.html')

# 👇 THIS IS THE CORRECTED ROUTE
@pages_bp.route('/tasks-page') # You were missing this line
@jwt_required(locations=['cookies']) # This protects the page from non-logged-in users
def tasks_page():
    # This renders your main dashboard HTML file
    return render_template("tasks.html")