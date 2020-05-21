from .job import JobApi, JobsApi
from .auth import SignupApi, LoginApi
from .user import UserApi
from .files import ResumeApi, CoverLetterApi

def initialize_routes(api):
    api.add_resource(JobsApi, '/api/jobs')
    api.add_resource(JobApi, '/api/jobs/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/signin')
    api.add_resource(UserApi, '/api/user')
    api.add_resource(ResumeApi, '/api/resume/<job_id>')
    api.add_resource(CoverLetterApi, '/api/coverletter/<job_id>')
