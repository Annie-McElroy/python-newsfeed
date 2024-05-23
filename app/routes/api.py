from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# Signup/Create new user
@bp.route('/users', methods=['POST'])
def signup():
  # connect to database
  data = request.get_json()
  db = get_db()
  
  try:
    # create new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # save in database
    db.add(newUser)
    db.commit()
  except:
    # creation failed, print error
    print(sys.exc_info()[0])

    # rollback and send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500
  
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

# Logout
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove sessions
  session.clear()
  return '', 204

# Login
@bp.route('/users/login', methods=['POST'])
def login():
  # connect to database
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data ['email']).one()
  except:
    print(sys.exc_info()[0])

    return jsonify(message = 'Incorrect credentials'), 400
  
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400
  
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

# Create new comment
@bp.route('/comments', methods=['POST'])
def comment():
  # connect to database
  data = request.get_json()
  db = get_db()

  try:
    # new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    # adds newComment to the database
    db.add(newComment)
    # commits database update
    db.commit()
  except:
    print(sys.exc_info()[0])

    # discards pending comment
    db.rollback()
    return jsonify(message = 'Comment failed'), 500
  
  return jsonify(id = newComment.id)

# Update Upvote
@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # discard pending upvote
    db.rollback()
    return jsonify(message ='Upvote failed'), 500
  
  return '', 204

# Create Post
@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db = get_db()

  try:
    # define new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # discard pending post
    db.rollback()
    return jsonify(message = 'Post failed'), 500
  
  return jsonify(id = newPost.id)
