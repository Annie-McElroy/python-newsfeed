from flask import session, redirect
from functools import wraps

# checks if logged in
def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    # if logged in, call original function with original args
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)
    
    #if not, redirect to login
    return redirect('/login')
  
  return wrapped_function