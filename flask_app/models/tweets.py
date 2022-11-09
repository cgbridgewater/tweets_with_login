from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash


### TWEET CONSTRUCTOR
class Tweet:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.creator = None # None can represent a currently empty space for a single User dictionary to be placed here, as a Tweet is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.comments = []


    ### TWEET GETTER AND ASSOCIATING A CREATER
    @classmethod
    def get_all_tweets_with_creator(cls):# Get all tweets, and their one associated User that created it
        query = '''
        SELECT * FROM tweets JOIN users ON tweets.user_id = users.id ORDER BY tweets.updated_at DESC;
        '''
        results = connectToMySQL('tweets_schema').query_db(query)
        all_tweets = []
        for row in results:# Create a Tweet class instance from the information from each db row
            one_tweet = cls(row)# Prepare to make a User class instance, looking at the class in models/user.py
            one_tweets_author_info = { # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            author = users.User(one_tweets_author_info)### Create the User class instance that's in the user.py model file
            one_tweet.creator = author ### Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            all_tweets.append(one_tweet) ### Append the Tweet containing the associated User to your list of tweets
        return all_tweets


    ### SAVE TWEET TO DB
    @classmethod
    def post_tweet(cls,data):
        query ='''
        INSERT INTO tweets (user_id, content) VALUES (%(user_id)s , %(content)s);
        '''
        return connectToMySQL('tweets_schema').query_db(query,data)


### TWEET VALIDATIONS
    @staticmethod
    def validate_post(tweet):
        is_valid = True # we assume this is true
        if len(tweet['content']) < 1:    ### email length check
            flash("Tweet post must not be blank!", "tweets")
            is_valid = False
        return is_valid ### if you make it this far, is good to go!


### DELETE TWEET BY ID (WORKING)
    @classmethod
    def delete_tweet(cls,data):
        query = "DELETE FROM tweets WHERE id = %(id)s;"
        return connectToMySQL('tweets_schema').query_db(query,data) 