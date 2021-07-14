from flask import Flask, jsonify, request, session, Response
from flask.helpers import make_response
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from development import SECRET_KEY, ALGORITHM
from bson.json_util import dumps, json
from bson import json_util, ObjectId
import jwt
import bcrypt
from flask_restx import Resource, Api, fields, reqparse, marshal
from flask_cors import CORS
from detection import get_img
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import boto3
from s3 import AWS_SECRET_KEY, AWS_ACCESS_KEY, BUCKET_NAME

app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록

app.secret_key=SECRET_KEY
CORS(app, supports_credentials=True)

nested_fields = {}
nested_fields["_id"]= fields.String()
nested_fields['title'] = fields.List(fields.String())
nested_fields["choices"] = fields.List(fields.String())
nested_fields["answer"] = fields.String()
nested_fields["script"] = fields.List(fields.String())
nested_fields["image"] = fields.String()
nested_fields["score"] = fields.String()
quizList_fields = {'quiz_list': fields.List(fields.Nested(api.model('nested', nested_fields)))}
showquiz_fields = api.model('ShowQuiz',{
  'data' : fields.List(fields.Nested(api.model('quizlist',quizList_fields)))
})

parser = reqparse.RequestParser()
signup_parser = reqparse.RequestParser()
login_parser = reqparse.RequestParser()
logout_parser= reqparse.RequestParser()
image_parser = reqparse.RequestParser()
qshow_parser = reqparse.RequestParser()
qmodify_parser = reqparse.RequestParser()
qdelete_parser = reqparse.RequestParser()

mongo = MongoClient('localhost', 27017) # 나중에 localhost를 mongo_db 로 바꾸기
#mongo = MongoClient('localhost', 27017)

db = mongo.Mandoo #Mandoo database
user = db.user   #user table
quiz = db.quiz   #quiz table

s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
#s3 = boto3.resource('s3')

@api.route('/hello')
class HelloWorld(Resource):
    @api.expect(parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    def get(self):  
        return "hello"


@api.route('/api/signup')
class Signup(Resource):
    signup_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    signup_parser.add_argument('name', required= True, location='json',type=str, help='사용자명')
    signup_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @api.expect(signup_parser)
    @api.response(201, '회원가입 성공')
    @api.response(400, 'Bad Request')
    @api.response(403, "아이디가 이미 있습니다")

    def post(self):
        
        new_user = request.json

        result = user.find_one({ "id" : new_user["id"] })   #user table에서 일치하는 아이디 검색
    
        if result :  #일치하는 아이디가 있음
            
            data = {
                "message": "아이디가 이미 있습니다",
                }
            response = jsonify(data)
            response.status_code = 403 
            return response 

        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt()) # 비밀번호 해싱
        
        user_info = {
            "id": new_user["id"],
            "name": new_user["name"],
            "password": new_user["password"],
            "quizzes" : []
        }
        user_id = user.insert_one(user_info).inserted_id

        data = {
            "success": True,
            "message" : "회원가입 성공",
            "id" : new_user["id"],
            "name" : new_user["name"]
            }
        response = jsonify(data)
        response.status_code = 201 
        return response 

       


@api.route('/api/login')
class login(Resource):

    login_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    login_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @api.expect(login_parser)
    @api.response(201, '로그인 성공')
    @api.response(400, 'Bad Request')
    @api.response(403, "해당 아이디가 없습니다\n 비밀번호가 틀렸습니다")
 
    def post(self):  
        login_user = request.json
        id = login_user['id']
       
        password = login_user['password']

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
        if result is None:  #일치하는 아이디가 없음
            data = {
                "message" : "해당 아이디가 없습니다",
            }
            response = jsonify(data)
            response.status_code = 403 
            return response 
        

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].decode("utf8").encode('utf-8')):
            id = result['id']
            payload = {
                'id' : id
            }
            token = jwt.encode(payload, SECRET_KEY, ALGORITHM)  #토큰 생성(인코딩)
            token = jwt.decode(token, SECRET_KEY, ALGORITHM)   #토큰 디코팅
    
            session['id'] = login_user['id']

            data = {
                "success": True,
                "message" : "로그인 성공",
                "accessToken": token['id'],
                "user_id" : login_user['id']
                }
            response = jsonify(data)
            response.status_code = 201 
            response.set_cookie('jwt', token['id'])
            return response 

        else:
            data = {
                "message" : "비밀번호가 틀렸습니다",
            }
            response = jsonify(data)
            response.status_code = 403
            return response 
            


@api.route('/api/logout')
class logout(Resource):

    @api.expect(logout_parser)
    @api.response(200, '로그아웃 성공')
    @api.response(400, 'Bad Request')

    def get(self):  
        session.pop('id',None)
        if request.cookies.get("jwt"):
            data = {
                "message" : "로그아웃 성공",
                "success": True
                }
            response = jsonify(data)
            response.status_code = 200 
            response.set_cookie("jwt", '', expires=0)
            return response 


@api.route('/api/imageupload')
class Image(Resource):
    
    image_parser.add_argument('image', type=FileStorage, required=True, location='files', help="문제 이미지")

    @api.expect(image_parser)
    @api.response(201, '이미지 등록 성공')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')

    def post(self):
        args = image_parser.parse_args()
        id = request.cookies.get('jwt')
        
        
        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
    
        if result is None:  #일치하는 아이디가 없음
            data = {
                "message": "로그인 필요"
            }
            response = jsonify(data)
            response.status_code = 401 
            return response

        img = args['image']
        
        imagefilename = id + ".png" # 서버 디렉토리에 저장하는 과정 (혹시 몰라서 추가)
        img.save('./upload/{0}'.format(secure_filename(imagefilename)))

        s3.put_object(Body='./upload/{0}'.format(secure_filename(imagefilename)), Bucket=BUCKET_NAME, Key=imagefilename)
        img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename


        title, choices, answer, script, image, score = get_img(id)
        user_id = session.get('id')
        
        processed_quiz = {
            "_id" : str(ObjectId()), # showquiz에서 return 시 ObjectId를 json 형태로 담기 위해 str 으로 변환해서 quiz 테이블에 insert 
            "title":title,
            "choices": choices,
            "answer": answer,
            "script" : script,
            "image" : image,
            "score" : score
        }
        quiz_id = quiz.insert_one(processed_quiz)
        author = user.find_one({"id":user_id})
        quiz_set = author['quizzes']
        quiz_set.append(ObjectId(processed_quiz["_id"])) # user 테이블에서는 quiz의 _id를 ObjectId 형태로 insert (str 도 가능하나 혹시 몰라서 ObjectId로 둠)
        user.update(
            {"id":user_id},
            {"$set" : {"quizzes":quiz_set}}
        )
        data = {
            "success": True,
            "message" : "이미지 등록 성공",
        }
        response = jsonify(data)
        response.status_code = 201 
        return response
        


@api.route('/api/showquiz')
class Showquiz(Resource):
    @api.expect(qshow_parser)
    @api.response(200, '퀴즈 리스트를 모두 가져옴', showquiz_fields)
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')

    def get(self):
        
        id = request.cookies.get('jwt')
        session_check = session.get('id')

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
    
        if result is None or session_check is None:  #일치하는 아이디가 없음
            data = {
                "message": "로그인 필요"
            }
            response = jsonify(data)
            response.status_code = 401
            return response


        user_id = session.get('id')
        author = user.find_one({"id":user_id}) # user테이블에서 퀴즈 가져오고자하는 사용자 찾음

        quiz_set = author['quizzes']    # 찾은 사용자에 연결된 퀴즈 _id 들을 quiz_set으로 가져옴
        quiz_list=[]
        for quiz_id in quiz_set:
            quiz_info = quiz.find_one({"_id":str(quiz_id)}) # quiz 테이블에서 사용자의 퀴즈를 하나씩 quiz_info로 받음
            quiz_list.append(quiz_info)

        data = {
            "success": True,
            "message": "퀴즈 리스트를 모두 가져옴",
            "quiz_list": quiz_list
            }
        response = jsonify(data)
        response.status_code = 200 
        return response



@api.route('/api/quizmodify')
class Quizmodify(Resource):

    qmodify_parser.add_argument('_id', required=True, location='json',type=str, help="quiz 아이디")
    qmodify_parser.add_argument('title', required=True, location='json',type=list, help="title")
    qmodify_parser.add_argument('choices', required=True, location='json',type=list, help="choices")
    qmodify_parser.add_argument('answer', required=True, location='json',type=str, help="answer")
    qmodify_parser.add_argument('script', required=True, location='json',type=list, help="script")
    qmodify_parser.add_argument('image', required=True, location='json',type=str, help="image") # 추후에 file type으로 변경 가능성 있음
    qmodify_parser.add_argument('score', required=True, location='json',type=str, help="image") 
    
    @api.expect(showquiz_fields)
    @api.response(201, '퀴즈 수정 성공')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')

    def put(self):
        
        id = request.cookies.get('jwt')
        session_check = session.get('id')

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
    
        if result is None or session_check is None:  #일치하는 아이디가 없음
            data = {
                "message": "로그인 필요"
            }
            response = jsonify(data)
            response.status_code = 401
            return response
        
        args = qmodify_parser.parse_args()
        print(args)
        

        quiz_id = args['_id']   #str 타입으로 req 요청된 상태
        title = args['title']
        choices = args['choices']
        answer = args['answer']
        script = args['script']
        image = args['image']
        score = args['score']

        quiz.update(
            { "_id" : quiz_id },
            { "$set" : { "title" : title, "choices" : choices ,"answer" : answer,"script" : script,"image" : image,"score" : score}}
        )

        data = {
            "success": True,
            "message": "퀴즈 수정 성공"
        }
        response = jsonify(data)
        response.status_code = 201 
        return response
        

@api.route('/api/quizdelete')
class Quizdelete(Resource):

    qdelete_parser.add_argument('quiz_id', required=True, location='json',type=str, help="quiz 아이디")

    @api.expect(qdelete_parser)
    @api.response(201, '퀴즈 삭제 성공')
    @api.response(400, 'Bad Request')
    @api.response(401, '로그인 필요')
    @api.response(403, '해당 퀴즈가 퀴즈 테이블에 없습니다\n퀴즈를 소유하고 있지 않습니다')
    def delete(self):
        
        id = request.cookies.get('jwt')
        session_check = session.get('id')

        result = user.find_one({ "id" : id })   #user table에서 일치하는 아이디 검색
    
        if result is None or session_check is None:  #일치하는 아이디가 없음
            data = {
                "message": "로그인 필요"
            }
            response = jsonify(data)
            response.status_code = 401 
            return response

        
        args = qdelete_parser.parse_args()
        quiz_id = args['quiz_id']   #str 타입으로 req 요청된 상태
        del_quiz = quiz.find_one({"_id":quiz_id}) # 삭제하고자하는 퀴즈가 quiz 테이블에 있는지 확인

        if del_quiz is None:
            data = {
                "message": "해당 퀴즈가 퀴즈 테이블에 없습니다"
            }
            response = jsonify(data)
            response.status_code = 403 
            return response

            
        user_id = session.get('id')
        author = user.find_one({"id":user_id})  #quiz 삭제를 요청한 사용자의 아이디 author로 얻음
        check_quiz_id = 0
        
        for owned_quiz in author['quizzes']:    # 삭제하기 전, quiz 삭제를 요청한 유저가 해당 quiz를 소유하고 있는지 확인하는 과정
            if ObjectId(quiz_id) == owned_quiz:
                check_quiz_id = 1  
        
        if check_quiz_id == 1:               # 유저가 해당 quiz를 소유하고 있다면
            quiz.delete_one({'_id':quiz_id}) # quiz 테이블에서 quiz 삭제
            author['quizzes'].remove(ObjectId(quiz_id)) # user 의 quizzes list 에서 quiz 삭제
            quiz_set = author['quizzes']     # 삭제가 반영된 quiz_set을 다시 user의 quizzes에 업데이트하기 위한 과정
            user.update(
                {"id":user_id},
                {"$set" : {"quizzes":quiz_set}}
            )

            data = {
                "success": True,
                "message": "퀴즈 삭제 성공"
            }
            response = jsonify(data)
            response.status_code = 201
            return response


        if check_quiz_id == 0:              # 유저가 해당 quiz를 소유하고 있지 않다면

            data = {
                "message": "퀴즈를 소유하고 있지 않습니다"
            }
            response = jsonify(data)
            response.status_code = 403 
            return response

           

#app.run(host='0.0.0.0',debug=True)
if __name__ =="__main__":
    app.config['SESSION_TYPE']='filesystem'
    app.run(host='0.0.0.0',debug=True)

