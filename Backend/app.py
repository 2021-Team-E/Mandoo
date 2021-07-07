from flask import Flask, jsonify, request, session
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
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
signup_parser.add_argument('name', required= True, location='json',type=str, help='사용자명')
signup_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

login_parser = reqparse.RequestParser()
login_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
login_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")


mongo = MongoClient('localhost', 27017) # 나중에 localhost를 mongo_db 로 바꾸기
#mongo = MongoClient('localhost', 27017)

db = mongo.Mandoo #Mandoo database
user = db.user   #user table
quiz = db.quiz   #quiz table


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
    @api.expect(signup_parser)
    def post(self):
        #회원가입에서 중복 아이디 확인하는 기능은 아직 없음
        new_user = request.json
        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt()) # 비밀번호 해싱
        
        user_info = {
            "id": new_user["id"],
            "name": new_user["name"],
            "password": new_user["password"],
            "quizzes" : []
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
    @api.expect(login_parser)
    def post(self):  
        login_user = request.json
        id = login_user['id']
        password = login_user['password']

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
    
        if result is None:  #일치하는 아이디가 없음
            return jsonify({
                "status": 401,
                "success": False,
                "message": "해당 아이디가 없습니다"
            }) 

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].decode("utf8").encode('utf-8')):
            id = result['id']
            payload = {
                'id' : id
            }
            token = jwt.encode(payload, SECRET_KEY, ALGORITHM)  #토큰 생성(인코딩)
            #token = jwt.decode(token, SECRET_KEY, ALGORITHM)   #토큰 디코팅

            session['id'] = id
           
            return jsonify({
            "status": 200,
            "success": True,
            "message" : "로그인 성공",
            "data" : { 
                "accessToken": token,
                "user_id" : login_user['id']
                }
            })
        else:
            return jsonify({
            "status": 401,
            "success": False,
            "message": "비밀번호가 틀렸습니다."
            })


@app.route('/quizupload', methods=['POST'])
def upload():
    id = get_user_id(request)
    if id is None:
        return jsonify({
            "status": 401,
            "success": False,
            "message": "로그인 필요"
        })
    if request.method == 'POST':
        img = request.json['image']
        title, choices, answer, script, image = get_img(img)
        user_id = session.get('id')
        processed_quiz = {
            "title":title,
            "choices": choices,
            "answer": answer,
            "script" : script,
            "image" : image
        }
        quiz_id = quiz.insert_one(processed_quiz).inserted_id
        author = user.find_one({"id":user_id})
        quiz_set = author['quizzes']
        quiz_set.append(quiz_id)
        user.update(
            {"id":user_id},
            {"$set" : {"quizzes":quiz_set}}
        )
        return jsonify({
            "status": 200,
            "success": True,
            "message": "퀴즈 등록 성공."
        })
        



#app.run(host='0.0.0.0',debug=True)
if __name__ =="__main__":
    app.config['SESSION_TYPE']='filesystem'
    app.run(host='0.0.0.0',debug=True)

