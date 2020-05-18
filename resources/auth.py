from flask import Response, request
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restful import Resource
import datetime
import json

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise NoAuthorizationError
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token, 'user': json.loads(User.objects.exclude('password').get(email=body.get('email')).to_json()) }, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError
