from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


@app.route('/recipes/new')
def new_recipe_form():
    if "user_id" not in session:
        return redirect ('/')
    return render_template("recipes_new.html")

@app.route('/recipes/create', methods =['post']) #this route will create a new recipe
def create_recipe():
    if "user_id" not in session:
        return redirect ('/')
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(recipe_data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>/view') #this route will select and view recipe
def get_one_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    one_recipe = Recipe.get_one(data)
    logged_user = User.get_by_id({'id': session['user_id']})

    return render_template("recipes_one.html", one_recipe = one_recipe, logged_user=logged_user)


@app.route('/recipes/<int:id>/edit') #this route will select and edit
def edit_recipe_form(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    one_recipe = Recipe.get_one(data)
    return render_template("recipes_edit.html", one_recipe = one_recipe)

@app.route('/recipes/<int:id>/update', methods = ['post']) 
def update_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    update_data = {
        **request.form,
        'id':id
    }
    # this_recipe = Recipe.get_one(update_data)
    # if not this_recipe.user_id == session ['user_id']:
    #     flash ('You can only update your recipe')
    #     return redirect("/dashboard")
    Recipe.update(update_data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    # this_recipe = Recipe.get_one(data)
    # if not this_recipe.user_id == session ['user_id']:
    #     flash ('You can only update your recipe')
    #     return redirect ('/dashboard')
    Recipe.delete(data)
    return redirect('/dashboard')