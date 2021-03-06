from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import datetime
from database.models import User
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError

class SignupApi(Resource):
  def post(self):
    try:
      body = request.get_json()
      user = User(**body)
      user.hash_password()
      user.save()
      return user, 200
    except FieldDoesNotExist:
      raise SchemaValidationError
    except NotUniqueError:
      raise EmailAlreadyExistsError
    except Exception as e:
      raise InternalServerError

class LoginApi(Resource):
  def post(self):
    try:
      body = request.get_json()
      user = User.objects.get(email=body.get('email'))
      authorized = user.check_password(body.get('password'))
      if not authorized:
        return {'error': 'Email or password invalid'}, 401
    
      expires = datetime.timedelta(days=7)
      access_token = create_access_token(identity=str(user.id), expires_delta=expires)
      res_data = {
        'token': access_token,
        'user': user.to_json()
      }
      return res_data, 200
    except (UnauthorizedError, DoesNotExist):
      raise UnauthorizedError
    except Exception as e:
      raise InternalServerError
