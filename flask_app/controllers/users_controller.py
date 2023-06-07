from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/users/register', methods = ['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/')
        # if not valid, send back to register
    # hashing the pass
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass,
    }
    #creating account with hashed pass
    logged_user_id = User.create(data)
    #storing the users id in session to consider them logged 
    session ['user_id'] = logged_user_id
    return redirect('/dashboard')
 
@app.route('/users/login', methods = ['POST'])
def log_user():
    data = {
        'email': request.form ['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credential", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credential", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/users/logout')
def log_out():
    # deleting user_id from session logs user out
    del session['user_id']
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    #this checks if user is not logged in and redirects them if so
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    context = {
        'logged_user' : logged_user,
        'all_recipes' : all_recipes
    }
    # logged_user = user.get_by_id ({'id': session ['user_id']})
    return render_template("welcome.html", **context)