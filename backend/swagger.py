from flask import Flask, jsonify, request, session, Response
from flask.helpers import make_response
from werkzeug.utils import secure_filename
from app import app
from flask_restplus import Api, Resource, fields

api = Api(app, title='QUIZRIX API')  # Flask 객체에 Api 객체 등록
ns  = api.namespace('api', description='API') # /detect/ 네임스페이스를 만든다

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


@ns.route('/hello')
class HelloWorld(Resource):

    @ns.expect(parser)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request')

    # @common_counter

    def get(self):  
        pass
       

@ns.route('/api/signup')
class Signup(Resource):

    signup_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    signup_parser.add_argument('name', required= True, location='json',type=str, help='사용자명')
    signup_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @ns.expect(signup_parser)
    @ns.response(201, '회원가입 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(403, "아이디가 이미 있습니다")

    # @common_counter

    def post(self):
        pass

       


@ns.route('/api/login')
class login(Resource):

    login_parser.add_argument('id', required=True, location='json',type=str, help='아이디')
    login_parser.add_argument('password', required=True, location='json',type=str, help="비밀번호")

    @ns.expect(login_parser)
    @ns.response(201, '로그인 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(403, "해당 아이디가 없습니다\n 비밀번호가 틀렸습니다")
    # @common_counter

    def post(self):  
        pass
            


@ns.route('/api/logout')
class logout(Resource):

    @ns.expect(logout_parser)
    @ns.response(200, '로그아웃 성공')
    @ns.response(400, 'Bad Request')

    # @common_counter

    def get(self):  
        pass


@ns.route('/api/imageupload')
class Image(Resource):
    
    image_parser.add_argument('image', type=FileStorage, required=True, location='files', help="문제 이미지")

    @ns.expect(image_parser)
    @ns.response(201, '이미지 등록 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(401, '로그인 필요')

    # @common_counter

    def post(self):
        pass
        


@ns.route('/api/showquiz')
class Showquiz(Resource):

    @ns.expect(qshow_parser)
    @ns.response(200, '퀴즈 리스트를 모두 가져옴', showquiz_fields)
    @ns.response(400, 'Bad Request')
    @ns.response(401, '로그인 필요')

    # @common_counter

    def get(self):
        pass


@ns.route('/api/quizmodify')
class Quizmodify(Resource):

    qmodify_parser.add_argument('_id', required=True, location='json',type=str, help="quiz 아이디")
    qmodify_parser.add_argument('title', required=True, location='json',type=list, help="title")
    qmodify_parser.add_argument('choices', required=True, location='json',type=list, help="choices")
    qmodify_parser.add_argument('answer', required=True, location='json',type=str, help="answer")
    qmodify_parser.add_argument('script', required=True, location='json',type=list, help="script")
    qmodify_parser.add_argument('image', required=True, location='json',type=str, help="image") # 추후에 file type으로 변경 가능성 있음
    qmodify_parser.add_argument('score', required=True, location='json',type=str, help="image") 
    
    @ns.expect(showquiz_fields)
    @ns.response(201, '퀴즈 수정 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(401, '로그인 필요')

    # @common_counter

    def put(self):
        pass

@ns.route('/api/quizdelete')
class Quizdelete(Resource):

    qdelete_parser.add_argument('quiz_id', required=True, location='json',type=str, help="quiz 아이디")

    @ns.expect(qdelete_parser)
    @ns.response(201, '퀴즈 삭제 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(401, '로그인 필요')
    @ns.response(403, '해당 퀴즈가 퀴즈 테이블에 없습니다\n퀴즈를 소유하고 있지 않습니다')

    # @common_counter

    def delete(self):
        pass
      