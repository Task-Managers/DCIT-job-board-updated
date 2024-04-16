from flask_jwt_extended import create_access_token,set_access_cookies, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User, Admin, Alumni, Company, Listing
from App.controllers import get_user_by_username

from flask import jsonify

# def login(username, password):
#   user = User.query.filter_by(username=username).first()
#   if user and user.check_password(password):
#     return create_access_token(identity=username)
#   return None

def login_user(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
    # if user is not None:
      token = create_access_token(identity=username)
      response = jsonify(access_token=token)
      set_access_cookies(response, token)
      return response
    # return jsonify(message="Invalid username or password"), 401
    return None

def login(username, password):
  # user = User.query.filter_by(username=username).first()
  user = get_user_by_username(username)
  
  if user and user.check_password(password):
    token = create_access_token(identity=username)
    print('token created')
    return (token)
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    # user = User.query.filter_by(username=identity).one_or_none()
    # if user:
    #     return user.id
    admin = Admin.query.filter_by(username=identity).one_or_none()
    if admin:
      return admin.username
        # return admin.id

    alumni = Alumni.query.filter_by(username=identity).one_or_none()
    if alumni:
      return alumni.username
      # return alumni.id

    company = Company.query.filter_by(username=identity).one_or_none()
    if company:
      return company.username
      # company.id

    return None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    # return User.query.get(identity)

    admin = Admin.query.filter_by(username=identity).one_or_none()
      # admin = Admin.query.get(identity)
    if admin:
      return admin

    alumni = Alumni.query.filter_by(username=identity).one_or_none()
    # alumni = Alumni.query.get(identity)
    if alumni:
      return alumni

    company = Company.query.filter_by(username=identity).one_or_none()
    # company = Company.query.get(identity)
    if company:
      return company
  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          # user_id = get_jwt_identity()
          # current_user = User.query.get(user_id)
          username = get_jwt_identity()
          current_user = get_user_by_username(username)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)