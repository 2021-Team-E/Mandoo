from flask import Flask, jsonify, request, session
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util
from development import SECRET_KEY, ALGORITHM
import jwt
import bcrypt
from flask_cors import CORS

from detection import get_img


app = Flask(__name__)
app.secret_key=SECRET_KEY
CORS(app)

#mongo = MongoClient('mongo_db', 27017)
mongo = MongoClient('localhost', 27017)
db = mongo['mandoo']
quizzes = db.quizzes
users = db.users

def get_user_id(request):
    token = request.headers.get('Authorization')
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

    return payload['id']

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/adduser')
def adduser():
    user = {
        "id" : "yyyyyyyyggy",
        "name" : "yoonjae",
        "password": "yoonjae",
        "questions": []
    }
    users.insert_one(user)
    session['id'] = 'yoonjae'
    user_result = users.find({"_id":"yoonjae"})
    result = dumps(user_result, default=json_util.default)
    return jsonify(result=result)

@app.route('/quizupload', methods=['POST'])
def upload():
    """
    id = get_user_id(request)
    if id is None:
        return jsonify({
            "status": 401,
            "success": False,
            "message": "로그인 필요"
        })"""
    if request.method == 'POST':
        img = request.json['image']
        title, choices, answer, script, image = get_img(img)
        user = session.get('id')
        quiz = {
            "title":title,
            "choices": choices,
            "answer": answer,
            "script" : script,
            "image" : image
        }
        quiz_id = quizzes.insert_one(quiz).inserted_id
        author = users.find_one({"_id":user})
        quiz_set = author['questions']
        quiz_set.append(quiz_id)
        users.update(
            {"_id":user},
            {"$set" : {"questions":quiz_set}}
        )
        user_result = users.find({"_id":user})
        result = dumps(user_result, default=json_util.default)
        return jsonify(result=result)


@app.route('/mongo', methods=['GET'])
def mongo_fetch():
    db = mongo.netflix
    netflix = db.netflix_titles.find()
    result = dumps(netflix, default=json_util.default)
    return jsonify(result=result)


@app.route('/mongo/kpop', methods=['GET'])
def mongo_kpop_fetch():
    db = mongo.kpop
    girl_grops = db.kpop_idols_girl_groups.find()
    result = dumps(girl_grops, default=json_util.default)
    return jsonify(result=result)


if __name__ =="__main__":
    app.config['SESSION_TYPE']='filesystem'
    app.run(host='0.0.0.0',debug=True)
