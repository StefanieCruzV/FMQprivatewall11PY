from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
NAME =re.compile(r'^[a-zA-Z ]+$' )
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Login:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.to_users = []
      
    # Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        query = "INSERT INTO login ( first_name , last_name , email , password ) VALUES ( %(first_name)s , %(last_name)s , %(email)s  , %(password)s)"
        # los nombres deben ser los de la bd / los valores los del html
        return connectToMySQL('login').query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM login WHERE email = %(email)s;"
        results = connectToMySQL("login").query_db(query,data)
        # Didn't find a matching user
        if len(results) < 1: #Si me devuelve algun row, el arreglo va a tener este row de la DB
            return False
        return cls(results[0]) # crea un objecto/instancia de la clase Login
    
    @classmethod
    def get_all_user_info(cls, data):
        query = "SELECT * FROM login WHERE id = %(id)s;"
        results = connectToMySQL("login").query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_all_user_db(cls, data):
        query = "SELECT * FROM login WHERE id != %(id)s"
        results = connectToMySQL("login").query_db(query,data)
        user_list = []
        for row_from_db in results:
            data = {
                "id": row_from_db["id"],
                "first_name": row_from_db['first_name'],
                "last_name": row_from_db['last_name'],
                "email": row_from_db['email'],
                "password": row_from_db['password']
            }
            user_list.append(cls(data))
        return user_list
    
    @classmethod
    def create_message(cls, data):
        print(data)
        query = "INSERT INTO message (message) values (%(message)s);"
        result = connectToMySQL("login").query_db(query,data)
        return result

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not NAME.match(user['first_name']):
            flash("Name must be only characters.")
            is_valid = False
        if  len(user['first_name']) < 2:
            flash("Name must be at least 2 .")
            is_valid = False
        if not NAME.match(user['last_name']):
            flash("Last name must be only characters.")
            is_valid = False
        if  len(user['first_name']) < 2:
            flash("Last ame must be at least 2 .")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8 :
            flash("Password must be at least 8 characters.")
            is_valid = False
        if len(user['con_password']) == 0:
            flash("must ned the confirmation")
            is_valid = False
        if user['password'] != user['con_password']:
            flash("Confirmation must match the password")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(form['password']) < 8 :
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid