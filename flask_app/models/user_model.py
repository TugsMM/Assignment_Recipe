from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import recipe_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User: 
    def __init__(self,data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.password = data ['password']
        self.email = data ['email']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @classmethod
    def create (cls,data):
        query= """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        # inserting above informations to users 
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users
            LEFT JOIN recipes ON recipes.user_id = users.id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            user_instance = cls(results[0])
            recipe_list = []
            for row in results:
                recipe_data = {
                    **row,
                    'id': row['recipes.id'],
                    'created_at': row['recipes.created_at'],
                    'updated_at': row['recipes.updated_at']
                }
                print (recipe_data)
                this_recipe_instance = recipe_model.Recipe(recipe_data)
                recipe_list.append(this_recipe_instance)
            user_instance.recepies = recipe_list
            return user_instance
        return False

    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2: # if first name's length is less than 2 show message below
            flash("first name must be at least 2 chars", 'reg')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("last name must be at least 2 chars", 'reg')
            is_valid = False
        if len(form_data['email']) < 1:
            flash("email required", 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("email invalid", 'reg')
            is_valid = False
        else:
            data = {
                'email': form_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("email already exitst (hope it's you!)", 'reg')
                is_valid = False
        if len(form_data['password']) < 8:
            flash("passowrd must be 8 chars", 'reg')
            is_valid = False
        elif not form_data['password'] == form_data['conf_pass']:
            flash("password must match", 'reg')
            is_valid = False

        return is_valid