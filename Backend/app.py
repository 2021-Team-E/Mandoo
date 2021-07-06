from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util


app = Flask(__name__)

#docker-compose 사용시
mongo = MongoClient('mongo_db', 27017)
# 로컬호스트 사용시
# mongo = MongoClient('localhost',27017)

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'


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


# app.run(host='0.0.0.0',debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
