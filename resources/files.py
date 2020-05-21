from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from resources.exceptions import UnauthorizedError
from database.models import Job, User
from flask_restful import Resource

class ResumeApi(Resource):
    @jwt_required
    def get(self, job_id):
        try:
            user_id = get_jwt_identity()
            job = Job.objects.get(id=job_id, added_by=user_id)
            return Response(job.resume.read(), mimetype="application/pdf", content_type=job.coverletter.content_type, status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError

class CoverLetterApi(Resource):
    @jwt_required
    def get(self, job_id):
        try:
            user_id = get_jwt_identity()
            job = Job.objects.get(id=job_id, added_by=user_id)
            return Response(job.coverletter.read(), mimetype="application/pdf", content_type=job.coverletter.content_type, status=200)
        except (NoAuthorizationError, Exception):
            raise UnauthorizedError
