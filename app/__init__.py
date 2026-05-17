from flask import Flask
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec

application = Flask(__name__)
application.secret_key = 'quiz-secret'

api = Api(application)
docs = FlaskApiSpec(application)