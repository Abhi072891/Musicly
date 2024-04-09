from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model import db, User, Role

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('age', type=int)
        parser.add_argument('gender', type=str)
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password_hash', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first() is not None:
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=args['email']).first() is not None:
            return {'message': 'Email already exists'}, 400
        role=Role.query.get(1)
        new_user = User(**args)
        new_user.set_password(args['password_hash'])
        db.session.add(new_user)
        new_user.roles.append(role)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    
def check_username_availability(username):
    username_=username
    user = User.query.filter_by(username=username_).first()
    if user:
        return {'available': False}, 201
    else:
        return {'available': True}, 400
    
def check_email_availability(email):
    email_=email
    user=User.query.filter_by(email=email_).first()
    if user:
        return {'available': False}, 201
    else:
        return {'available': True}, 400

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password_hash', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user and user.check_password(args['password_hash']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token,
                    'user_id':user.id,
                    'user_role':user.roles[0].name}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

class AdminLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password_hash', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        admin = User.query.filter_by(username=args['username'], role='admin').first()

        if admin and admin.check_password(args['password_hash']):
            access_token = create_access_token(identity=admin.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        data=get_jwt_identity()
        print(data)
        return {'message': 'Protected resource'}, 200