from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)
#@auth.route("hello")

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form #data has type dict
    print(data) 
    if request.method=='POST':
        email = request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('log in successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password',category='error')
    
        else:
            flash('user doesnt exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required ##decorater
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
## Get data from signup form
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User exists', category='error')
        ## check if input credentials are valid
        elif len(email) < 4:
            flash('Email ID should be greater than 4', category='error')
        elif len(first_name) < 2:
            flash('First name incorr', category = 'error')
        elif password1 != password2:
            flash('passwords dont match', category = 'error')
        elif len(password1) < 7:
            flash('password should be > 7', category = 'error')
        else:

            new_user = User(email=email,first_name=first_name,password = generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('account successfuly created', category = 'success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

            # add user to database
        ## for flashing message



    return render_template("sign_up.html", user=current_user)