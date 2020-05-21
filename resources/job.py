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
            body = request.form.to_dict()
            user = User.objects.get(id=user_id)
            job = Job(**body, added_by=user)
            files = request.files.to_dict()
            for file in files:
                job[file].put(request.files[file], content_type = 'application/pdf')
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
            body = request.form.to_dict()
            job.update(**body)
            files = request.files.to_dict()
            for file in files:
                job[file].replace(request.files[file], content_type = 'application/pdf')
            job.save()
            return {'updated': True}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            job = Job.objects.get(id=id, added_by=user_id)
            job.delete()
            return {'deleted': True}, 200
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

    @jwt_required
    def get(self, id):
        try:
            job = Job.objects.get(id=id).to_json()
            return Response(job, mimetype="application/json", status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError
