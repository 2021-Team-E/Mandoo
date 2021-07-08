from flask import Flask, jsonify, request, session
from flask.helpers import make_response
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
CORS(app, supports_credentials=True)

parser = reqparse.RequestParser()

signup_parser = reqparse.RequestParser()
login_parser = reqparse.RequestParser()
logout_parser= reqparse.RequestParser()
image_parser = reqparse.RequestParser()
quiz_parser = reqparse.RequestParser()
qmodify_parser = reqparse.RequestParser()

mongo = MongoClient('localhost', 27017) # 나중에 localhost를 mongo_db 로 바꾸기
#mongo = MongoClient('localhost', 27017)

db = mongo.Mandoo #Mandoo database
user = db.user   #user table
quiz = db.quiz   #quiz table


@api.route('/hello')
class HelloWorld(Resource):
    @api.expect(parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    def get(self):  
        return "hello"


@api.route('/signup')
class Signup(Resource):

    signup_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    signup_parser.add_argument('name', required= True, location='json',type=str, help='사용자명')
    signup_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @api.expect(signup_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(403, "아이디가 이미 있습니다.")

    def post(self):
        
        new_user = request.json

        result = user.find_one({ "id" : new_user["id"] })   #user table에서 일치하는 아이디 검색
    
        if result :  #일치하는 아이디가 있음
            return jsonify({
                "status": 403,
                "success": False,
                "message": "아이디가 이미 있습니다."
            }) 

        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt()) # 비밀번호 해싱
        
        user_info = {
            "id": new_user["id"],
            "name": new_user["name"],
            "password": new_user["password"],
            "quizzes" : []
        }
        user_id = user.insert_one(user_info).inserted_id

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

    login_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    login_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @api.expect(login_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(403, "해당 아이디가 없습니다.\n 비밀번호가 틀렸습니다.")
 
    def post(self):  
        login_user = request.json
        id = login_user['id']
        password = login_user['password']

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
        if result is None:  #일치하는 아이디가 없음
            return jsonify({
                "status": 403,
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

            session['id'] = login_user['id']
           
            out = jsonify({
                "status": 200,
                "success": True,
                "message" : "로그인 성공",
                "data" : { 
                    "accessToken": token,
                    "user_id" : login_user['id']
                    }
            })
            out.set_cookie('jwt', token)
            #session['jwt'] = token

            return out

        else:
            return jsonify({
                "status": 403,
                "success": False,
                "message": "비밀번호가 틀렸습니다."
            })


@api.route('/logout')
class logout(Resource):

    @api.expect(logout_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')

    def post(self):  
        session.pop('id',None)
        return jsonify({
                "status": 200,
                "success": True,
                "message": "로그아웃 성공"
        })

@api.route('/quizupload')
class Image(Resource):
    
    image_parser.add_argument('image', required=True, location='files', help="문제 이미지")

    @api.expect(image_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')

    def post(self):
        args = image_parser.parse_args()
        id = request.cookies.get('jwt')
        #id = session.get('jwt')
        if id is None:
            return jsonify({
                "status": 401,
                "success": False,
                "message": "로그인 필요"
            })
        img = args['image']
        title, choices, answer, script, image = get_img(img)
        user_id = session.get('id')
        
        processed_quiz = {
            "_id" : str(ObjectId()), # showquiz에서 return 시 ObjectId를 json 형태로 담기 위해 str 으로 변환해서 quiz 테이블에 insert 
            "title":title,
            "choices": choices,
            "answer": answer,
            "script" : script,
            "image" : image
        }
        quiz_id = quiz.insert_one(processed_quiz)
        author = user.find_one({"id":user_id})
        quiz_set = author['quizzes']
        quiz_set.append(ObjectId(processed_quiz["_id"])) # user 테이블에서는 quiz의 _id를 ObjectId 형태로 insert (str 도 가능하나 혹시 몰라서 ObjectId로 둠)
        user.update(
            {"id":user_id},
            {"$set" : {"quizzes":quiz_set}}
        )
        return jsonify({
            "status": 200,
            "success": True,
            "message": "퀴즈 등록 성공."
        })



@api.route('/showquiz')
class Showquiz(Resource):

    @api.expect(quiz_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')

    def get(self):
        
        id = request.cookies.get('jwt')
      
        if id is None:
            return jsonify({
                "status": 401,
                "success": False,
                "message": "로그인 필요"
            })

        user_id = session.get('id')
        author = user.find_one({"id":user_id}) # user테이블에서 퀴즈 가져오고자하는 사용자 찾음

        quiz_set = author['quizzes']    # 찾은 사용자에 연결된 퀴즈 _id 들을 quiz_set으로 가져옴
        quiz_list=[]
        for quiz_id in quiz_set:
            quiz_info = quiz.find_one({"_id":str(quiz_id)}) # quiz 테이블에서 사용자의 퀴즈를 하나씩 quiz_info로 받음
            quiz_list.append(quiz_info)
     
        return jsonify({
            "status": 200,
            "success": True,
            "message": "퀴즈 리스트를 모두 가져옴",
            "data" : {
                "quiz_list": quiz_list
            }
        })

@api.route('/quizmodify')
class Quizmodify(Resource):

    qmodify_parser.add_argument('_id', required=True, location='json',type=str, help="quiz 아이디")
    qmodify_parser.add_argument('title', required=True, location='json',type=str, help="title")
    qmodify_parser.add_argument('choices', required=True, location='json',type=list, help="choices")
    qmodify_parser.add_argument('answer', required=True, location='json',type=int, help="answer")
    qmodify_parser.add_argument('script', required=True, location='json',type=str, help="script")
    qmodify_parser.add_argument('image', required=True, location='json',type=str, help="image") # 추후에 file type으로 변경 가능성 있음

    @api.expect(qmodify_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')
    def post(self):
        
        id = request.cookies.get('jwt')
      
        if id is None:
            return jsonify({
                "status": 401,
                "success": False,
                "message": "로그인 필요"
            })

        args = qmodify_parser.parse_args()
        print(args)
        quiz_id = args['_id']   #str 타입으로 req 요청된 상태
        title = args['title']
        choices = args['choices']
        answer = args['answer']
        script = args['script']
        image = args['image']

        quiz.update(
            { "_id" : quiz_id },
            { "$set" : { "title" : title, "choices" : choices ,"answer" : answer,"script" : script,"image" : image}}
        )

     
        return jsonify({
            "status": 200,
            "success": True,
            "message": "퀴즈 수정 성공"
            
        })



#app.run(host='0.0.0.0',debug=True)
if __name__ =="__main__":
    app.config['SESSION_TYPE']='filesystem'
    app.run(host='0.0.0.0',debug=True)

