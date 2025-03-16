from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, current_user
from website.models import User, db

auth = Blueprint('auth', __name__)
ADMIN_EMAIL = "cutsbytrent@gmail.com"
ADMIN_PASSWORD = "dogs"

@auth.route('/sign-up')
def sign_up():
    return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['is_admin'] = True  # Set session variable for admin
            return redirect('/')  # Redirect to home page for admin

        # Check if it's a regular user (using email as the user identifier)
        user = User.query.filter_by(name=email).first()
        if user and user.password == password:
            session['is_admin'] = False  # Regular user, no admin rights
            return redirect('/')  # Redirect to home page for regular user

        flash('Invalid credentials, please try again.', category='error')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template("logout.html")