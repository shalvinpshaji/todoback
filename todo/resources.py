from todo import api, bcrypt
from flask import request, session, jsonify
from todo import app
from flask_restful import Resource, reqparse
from todo.models import db, User, Todo, List
parser = reqparse.RequestParser()
parser.add_argument('list')

def is_loggedin():
    print('inside login')
    if 'user_id' in session:
        print('true')
        return True
    print('false')
    return False


class SignIn(Resource):
    def post(self):
        data = request.get_json(force=True)
        print(data)
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        print(user)
        print(bcrypt.check_password_hash(user.password, password))
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user'] = user.email
            return {'isLoggedIn': True, 'status' : 'success'}
        return {'isLoggedIn': False, 'status' : 'fail'}

    
class SignUp(Resource):
    def post(self):
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        confirm = data['confirm']
        print(data)
        print(User.query.filter_by(email=email).first())
        if User.query.filter_by(email=email).first() == None and confirm == password:
            print('Inside user creation block')
            hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(email = email, password = hash)
            db.session.add(user)
            db.session.commit()
            user = User.query.all()[-1]
            session['user_id'] = user.id
            session['user'] = user.email
            response = jsonify({'isLoggedIn': True, 'status' : 'success'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        response = jsonify({'isLoggedIn': False, 'status' : 'fail'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class Lists(Resource):
    def get(self):
        print(is_loggedin())
        if is_loggedin():
            u_id = session['user_id']
            lists = List.query.filter_by(user_id = u_id)
            l = list(map(lambda l:l.name, lists))
            print(l)
            return {'lists': l, 'isLoggedIn': True, 'status': 'success'}
        return {'lists': [], 'isLoggedIn': False, 'status': 'fail'}
    
    def post(self):
        if is_loggedin():
            u_id = session['user_id']
            data = request.get_json(force=True)
            print(data)
            list = List(name = data['list'], user_id= u_id)
            db.session.add(list)
            db.session.commit()
            return {'status': 'success'}
        return {'status': 'fail'}

        
class Todo(Resource):
    def get(self, list_name):
        data = {}
        if is_loggedin():
            user_id = session['user_id']
            data = request.get_json(force=True)
            print(data)
            user = User.query.filter_by(id=user_id).first()
            current_list = list(filter(lambda l:l.name==list_name, user.lists))
            print(current_list)
            if current_list:
                data['todos'] = list(map(lambda x:x.item, current_list[0].todos))
                data['status'] = 'success'
                return data
        else:
            data['is_loggedin'] = False
        data['todos'] = []
        data['status'] = 'fail'
        print(data)
        return data

    def post(self, list_name):
        if is_loggedin():
            json_data = request.get_json(force=True)
            print(json_data)
            todo = json_data['todo']
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            l = list(filter(lambda l:l.name==list_name, user.lists))
            data = {}
            if l:
                todo = Todo(item=todo, user_id=user_id, list_id=l[0].id)
                db.session.add(todo)
                db.session.commit()
                return {'status': 'success'}
        return {'status': 'fail'}


api.add_resource(Todo, '/todo/<string:list_name>')
api.add_resource(SignIn, '/signin')
api.add_resource(SignUp, '/signup')
api.add_resource(Lists, '/list')

