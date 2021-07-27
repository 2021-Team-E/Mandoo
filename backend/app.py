from flask import Flask, jsonify, request, session, Response
from flask.helpers import make_response
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from development import SECRET_KEY, ALGORITHM
from bson.json_util import json
from bson import json_util, ObjectId
import jwt
import bcrypt

from flask_cors import CORS
from detection import get_img
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import boto3
from s3 import AWS_SECRET_KEY, AWS_ACCESS_KEY, BUCKET_NAME
import datetime, os

#prometheus
# import time
# from random import random
# from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# #prometheus
# metrics = PrometheusMetrics(app)
# metrics.info("flask_app_info", "App Info, this can be anything you want", version="1.0.0")

# # custom metric to be applied to multiple endpoints
# common_counter = metrics.counter(
#     'flask_by_endpoint_counter', 'Request count by endpoints',
#     labels={'endpoint': lambda: request.endpoint}
# )
#####
app.secret_key=SECRET_KEY
CORS(app, supports_credentials=True)
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
mongo = MongoClient('localhost', 27017) # 나중에 localhost를 mongo_db 로 바꾸기
#mongo = MongoClient('localhost', 27017)

db = mongo.Mandoo #Mandoo database
user = db.user   #user table
quiz = db.quiz   #quiz table

s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
#s3 = boto3.resource('s3')

@app.route('/hello',methods=['GET'])
def get():  

    return "hello"


@app.route('/api/signup', methods=['POST'])

 # @common_counter

def signup():
        
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

       


@app.route('/api/login' , methods=['POST'])

# @common_counter

def login():  

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
            


@app.route('/api/logout' , methods=['GET'])

# @common_counter

def logout():  

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


@app.route('/api/imageupload' , methods=['POST'])

# @common_counter

def imageupload():

    args = request.args
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
        
    if not os.path.exists('upload'):
        os.makedirs('upload')

    imagefilename = id + ".jpeg" # 서버 디렉토리에 저장하는 과정 (혹시 몰라서 추가)
    img.save('./upload/{0}'.format(secure_filename(imagefilename)))
    imagetoupload  = open('./upload/{0}'.format(secure_filename(imagefilename)), 'rb')

    imagefilename ="upload/"+ id + "_" + str(datetime.datetime.now())+".jpeg"
    imagefilename.replace(" ","")
        
    s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
    img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename 
    image = img_url              # 딥러닝 거치기 전의 이미지가 저장된 s3 주소 
    print(image)
    title, choices, answer, script, score = get_img(id)
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
        


@app.route('/api/showquiz' , methods=['GET'])

# @common_counter

def showquiz():
        
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



@app.route('/api/quizmodify' , methods=['PUT'])

# @common_counter

def quizmodify():
        
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
        
    args = request.args
        
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
        

@app.route('/api/quizdelete' , methods=['DELETE'])

# @common_counter

def quizdelete():
        
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
        
    args = request.args
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

# register additional default metrics
# metrics.register_default(
#     metrics.counter(
#         'flask_by_path_counter', 'Request count by request paths',
#         labels={'path': lambda: request.path}
#     )
# )

#app.run(host='0.0.0.0',debug=True)
if __name__ =="__main__":
    app.config['SESSION_TYPE']='filesystem'
    app.run(host='0.0.0.0',debug=True)

