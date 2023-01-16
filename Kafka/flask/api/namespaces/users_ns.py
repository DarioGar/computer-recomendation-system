import api.reusable
from flask_restx import Resource
from flask import jsonify, make_response
from flask_restx import cors
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from api.arguments.gpu_arguments import new_gpu_arguments
from api.reusable import get_hashed_password
from api.v1 import api
from core import limiter, cache

users_ns = api.namespace('gpu',description='Manages graphic card components',decorators=[cors.crossdomain(origin="*")])
