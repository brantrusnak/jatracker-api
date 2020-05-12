from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User
from flask_restful import Resource
import datetime


class UserApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.exclude('password').get(id=user_id).to_json()
        return Response(user, mimetype="application/json", status=200)

    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        User.objects.exclude('password').get(id=user_id).update(**body)
        return {'updated': True}, 200
