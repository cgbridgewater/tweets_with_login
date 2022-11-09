from flask_app import app
from flask import redirect, session, request
from flask_app.models.tweets import Tweet


@app.route("/dashboard/post/message", methods = (["POST"]))
def post_message():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        "content" : request.form['content']
        }     
    if not Tweet.validate_post(data):
        return redirect('/dashboard')
    Tweet.post_tweet(data)
    print(data)
    return redirect("/dashboard")


@app.route("/dashboard/message/delete", methods = (["POST"]))
def delete_message():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        "id" : request.form['tweets.id']
    }
    Tweet.delete_tweet(data)
    return redirect("/dashboard")