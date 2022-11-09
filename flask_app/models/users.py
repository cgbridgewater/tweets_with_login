from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


### USER CLASS
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']    
        self.password = data['password']    
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tweets = [] # [] can represent a currently empty place to store all of the tweets that a single User instance has created, as a User creates MANY Tweets 


### REGISTRATION VALIDATIONS
    @staticmethod
    def validate_registration(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2: ### first name length check
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2: ### first name length check
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['password']) < 3: ### password length check
            flash("Password must be a valid password.", "register")
            is_valid = False
        if len(user['confirm_password']) < 4: ### password length check
            flash("Password must be a valid password.", "register")
            is_valid = False
        if user['password'] != user['confirm_password']: #### passwords must match
            flash("Passwords must match!!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):  ### checks email formating
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['email']) < 3:    ### email length check
            flash("Email must be a valid email.", "register")
            is_valid = False
        if User.email_exists(user):  ### check user email is origional
            flash("This email is already taken!", "register")
            is_valid = False 
        return is_valid ### if you make it this far, is good to go!


### LOGIN VALIDATIONS
    @staticmethod
    def validate_login(user):
        is_valid = True # we assume this is true
        if len(user['email']) < 3:    ### email length check
            flash("Email must be a valid email.", "login")
            is_valid = False
        if len(user['password']) < 3: ### password length check
            flash("Password must be a valid password.", "login")
            is_valid = False
        return is_valid ### if you make it this far, is good to go!


### UPDATE VALIDATIONS
    @staticmethod
    def validate_update(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3: ### password length check
            flash("First name must be at least 3 charactors long.", "update")
            is_valid = False
        if len(user['last_name']) < 3: ### password length check
            flash("Last name must be at least 3 charactors long.", "update")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):  ### checks email formating
            flash("Invalid email address!", "update")
            is_valid = False
        return is_valid ### if you make it this far, is good to go!


### CHECK FOR EXISTING EMAIL (WORKING)
    @classmethod 
    def email_exists(cls,data):
        query = '''
        SELECT * FROM users WHERE email = %(email)s;
        '''
        result = connectToMySQL("tweets_schema").query_db(query,data)
        if len(result) < 1:
            return False   #didn't find a matching user
        return cls(result[0])


### CREATE AND SAVE NEW USER (WORKING)
    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );
        '''
        return connectToMySQL('tweets_schema').query_db(query,data)


### GET USER BY ID (WORKING)
    @classmethod
    def get_user_by_id(cls,data):
        query = '''
        SELECT * FROM users WHERE id = %(id)s;
        '''
        result = connectToMySQL('tweets_schema').query_db(query,data)
        if len(result) == 0: #if no users found, return an empty list
            return None
        else: # if at least one user found
            return cls(result[0])


### UPDATE USER BY ID (WORKING)
    @classmethod
    def update_user_by_id(cls,data):
        query = '''
        UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;
        '''
        return connectToMySQL('tweets_schema').query_db(query,data)


### DELETE USER BY ID (WORKING)
    @classmethod
    def delete_user(cls,data):
        query = '''
        DELETE FROM users WHERE id = %(id)s;
        '''
        return connectToMySQL('tweets_schema').query_db(query,data) 