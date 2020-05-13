from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from resources.exceptions import UnauthorizedError
from database.models import User
from flask_restful import Resource
import datetime

class UserApi(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            print('USERID', user_id)
            user = User.objects.exclude('password').get(id=user_id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            body = request.get_json()
            User.objects.exclude('password').get(id=user_id).update(**body)
            return {'updated': True}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError