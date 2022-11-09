from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash


### COMMENT CONSTRUCTOR
class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.tweet_id = data['tweet_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.creator = None #### None can represent a currently empty space for a single User dictionary to be placed here, as a Tweet is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.comments = []


### SAVE COMMENT TO DATABASE (WORKING)
    @classmethod
    def post_comment(cls,data):
        query ='''
        INSERT INTO comments (tweet_id , user_id , comment) VALUES (%(tweet_id)s , %(user_id)s , %(comment)s);
        '''
        return connectToMySQL('tweets_schema').query_db(query,data)


### COMMENT VALIDATION (WORKING)
    @staticmethod
    def validate_post(comment):
        is_valid = True # we assume this is true
        if len(comment['comment']) < 1:    ### email length check
            flash("Comment posts must not be blank!", "comments")
            is_valid = False
        return is_valid ### if you make it this far, is good to go!


### GET COMMENTS NEWEST FIRST (WORKING)
    @classmethod
    def get_all_comments_with_creator(cls):
        # Get all tweets, and their one associated User that created it
        query = '''
        SELECT * FROM users
        LEFT JOIN comments 
        ON comments.user_id = users.id ORDER BY comments.updated_at DESC;
        '''
        results = connectToMySQL('tweets_schema').query_db(query)
        all_comments = []
        for row in results:# Create a Tweet class instance from the information from each db row
            one_comment = cls(row)# Prepare to make a User class instance, looking at the class in models/user.py
            one_comments_author_info = { # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['comments.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "comment": row['comment'],
                "email": row['email'],
                "password": row['password'],
                "user_id": row['user_id'],
                "tweet_id": row['tweet_id'],
                "created_at": row['comments.created_at'],
                "updated_at": row['comments.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = users.User(one_comments_author_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_comment.creator = author
            # Append the Tweet containing the associated User to your list of tweets
            all_comments.append(one_comment)
        return all_comments


### DELETE USER BY ID (WORKING)
    @classmethod
    def delete_comment(cls,data):
        query = '''
        DELETE FROM comments WHERE id = %(id)s;
        '''
        return connectToMySQL('tweets_schema').query_db(query,data)