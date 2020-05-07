from .job import JobApi, JobsApi
from .auth import SignupApi, LoginApi


def initialize_routes(api):
    api.add_resource(JobsApi, '/api/jobs')
    api.add_resource(JobApi, '/api/jobs/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/signin')
