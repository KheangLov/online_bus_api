from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import json_util
from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, BusAlreadyExistsError, \
InternalServerError, UpdatingBusError, DeletingBusError, BusNotExistsError
from database.models import Bus, User

class BusesApi(Resource):
  def get(self):
    buses = Bus.objects().to_json()
    return Response(
      buses, 
      mimetype='application/json', 
      status=200
    )

  @jwt_required
  def post(self):
    try:
      user_iden = get_jwt_identity()
      body = request.get_json()
      user = User.objects.get(id=user_iden)
      bus = Bus(**body, user_id=user)
      resBus = bus.save()
      return resBus, 200
    except (FieldDoesNotExist, ValidationError):
      raise SchemaValidationError
    except NotUniqueError:
      raise BusAlreadyExistsError
    except Exception as e:
      raise InternalServerError
 
class BusApi(Resource):
  @jwt_required
  def put(self, id):
    try:
      user_iden = get_jwt_identity()
      bus = Bus.objects.get(id=id, user_id=user_iden)
      body = request.get_json()
      Bus.objects.get(id=id).update(**body)
      return {'status': 1}, 200
    except InvalidQueryError:
      raise SchemaValidationError
    except DoesNotExist:
      raise UpdatingBusError
    except Exception:
      raise InternalServerError
 
  @jwt_required
  def delete(self, id):
    try:
      user_iden = get_jwt_identity()
      bus = Bus.objects.get(id=id, user_id=user_iden)
      bus.delete()
      return {'status': 1}, 200
    except DoesNotExist:
      raise DeletingBusError
    except Exception:
      raise InternalServerError

  @jwt_required
  def get(self, id):
    try:
      buses = Bus.objects.get(id=id).to_json()
      return Response(buses, mimetype="application/json", status=200)
    except DoesNotExist:
      raise BusNotExistsError
    except Exception:
      raise InternalServerError
