from flask import Flask, jsonify, request, Blueprint, session
from pymongo import MongoClient
from development import SECRET_KEY, ALGORITHM
from bson.json_util import dumps
from bson import json_util, ObjectId
import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace, fields, reqparse
from flask_cors import CORS
from detection import get_img

app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록
app.secret_key=SECRET_KEY
CORS(app)
parser = reqparse.RequestParser()

mongo = MongoClient('localhost', 27017)

db = mongo['Mandoo']#Mandoo database
user = db['user']   #user table
quiz = db['quiz']   #quiz table

def get_user_id(request):
    token = request.headers.get('Authorization')
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

    return payload['id']

@api.route('/hello')
class HelloWorld(Resource):
    @api.expect(parser)
    def get(self):  
        return "hello"


@api.route('/signup')
class Signup(Resource):
    @api.expect(parser)
    def post(self):
        new_user = request.json

        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt()) # 비밀번호 해싱

        user_info = {
            "id": new_user["id"],
            "name": new_user["name"],
            "password": new_user["password"],
        }
        user_id = user.insert_one(user_info).inserted_id
        print(user_id)
        print(user_info)
        return jsonify({
            "status": 200,
            "success": True,
            "message" : "회원가입 성공",
            "data" : { 
                "id" : new_user["id"],
                "name" : new_user["name"]
            }
            
        })

@api.route('/login')
class login(Resource):
    @api.expect(parser)
    def post(self):  
        return "login"

app.run(host='0.0.0.0',debug=True)
