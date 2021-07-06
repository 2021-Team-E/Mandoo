from flask import Flask, jsonify, request, Blueprint, session
from pymongo import MongoClient

from bson.json_util import dumps
from bson import json_util, ObjectId
import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace, fields, reqparse


app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록
parser = reqparse.RequestParser()

mongo = MongoClient('localhost', 27017)

db = mongo['Mandoo'] #Mandoo database
user = db['user'] #user table


@api.route('/hello', methods=['GET'])
class HelloWorld(Resource):
    @api.expect(parser)
    def get(self):  
        return "hello"


@api.route('/signup', methods=['POST','GET'])
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

        return jsonify({
            "status": 200,
            "success": True,
            "message" : "회원가입 성공",
            "data" : { 
                "id" : new_user["id"],
                "name" : new_user["name"]
            }
            
        })
        
    def get(self):
        return "...."

# @app.route('/mongo', methods=['GET'])
# def mongo_fetch():
#     db = mongo.netflix
#     netflix = db.netflix_titles.find()
#     result = dumps(netflix, default=json_util.default)
#     return jsonify(result=result)


# @app.route('/mongo/kpop', methods=['GET'])
# def mongo_kpop_fetch():
#     db = mongo.kpop
#     girl_grops = db.kpop_idols_girl_groups.find()
#     result = dumps(girl_grops, default=json_util.default)
#     return jsonify(result=result)


app.run(host='0.0.0.0',debug=True)
