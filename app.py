from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_cors import CORS
from resources.exceptions import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['PROPAGATE_EXCEPTIONS'] = True

CORS(app=app, supports_credentials=True)

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/jatracker'
}

initialize_db(app)
initialize_routes(api)

app.run()
