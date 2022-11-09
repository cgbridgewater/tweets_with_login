from flask_app import app
from flask import redirect, session, request
from flask_app.models.comments import Comment


@app.route("/dashboard/post/comment", methods = (["POST"]))
def post_comment():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        "tweet_id" : request.form['tweet_id'],
        "comment" : request.form['comment']
        }     
    if not Comment.validate_post(data):
        return redirect('/dashboard')
    Comment.post_comment(data)
    print(data)
    return redirect("/dashboard")


@app.route("/dashboard/comment/delete", methods = (["POST"]))
def delete_comments():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        "id" : request.form['comments.id']
    }
    Comment.delete_comment(data)
    return redirect("/dashboard")