from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO recipes (recipe_name, description, instructions, date_cooked, under_30, user_id)
            VALUES (%(recipe_name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s)
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):   # this part is joining parties user it to users user id
        query = """
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
        """
        #            # WHERE recipes.id = %(id)s;
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data ={
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.planner = this_user
                all_recipes.append(this_recipe)
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query = """ 
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            row = results[0]
            this_recipe = cls(row)
            user_data ={
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_recipe.planner = this_user
            return this_recipe
        return False

    @classmethod
    def update(cls,data):
        query = """
            UPDATE recipes SET recipe_name = %(recipe_name)s, description = %(description)s,
            instructions = %(instructions)s, date_cooked = %(date_cooked)s,
            under_30 = %(under_30)s
            WHERE recipes.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete (cls, data):
        query = """
            DELETE FROM recipes WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['recipe_name']) < 3:
            flash('name must be at least 3 characters')
            is_valid = False
        if len(form_data['description']) < 3:
            flash('description must be at least 3 characters')
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash('instructions must be at least 3 characters')
            is_valid = False
        if len(form_data['date_cooked']) < 3:
            flash('Date Cooked must be at least 3 characters')
            is_valid = False
        if "under_30" not in form_data:
            flash('under 30 minutes required')
            is_valid = False
        return is_valid