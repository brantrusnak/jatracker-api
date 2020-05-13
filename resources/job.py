from flask import Response, request
from database.models import Job, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_jwt_extended.exceptions import NoAuthorizationError
from resources.exceptions import UnauthorizedError

class JobsApi(Resource):
    @jwt_required
    def get(self):
        try:
            query = Job.objects()
            jobs = Job.objects().to_json()
            return Response(jobs, mimetype="application/json", status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            job = Job(**body, added_by=user)
            job.save()
            user.update(push__jobs=job)
            user.save()
            id = job.id
            return {'id': str(id)}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError


class JobApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            job = Job.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Job.objects.get(id=id).update(**body)
            return {'updated': True}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def delete(self, id):
        try:
            pass
            user_id = get_jwt_identity()
            job = Job.objects.get(id=id, added_by=user_id)
            job.delete()
            return {'deleted': True}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def get(self, id):
        try:
            jobs = Job.objects.get(id=id).to_json()
            return Response(jobs, mimetype="application/json", status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError
