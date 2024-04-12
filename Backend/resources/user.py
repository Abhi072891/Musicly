from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model import db, User, Role, Song, Album
from sqlalchemy import or_

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
                    'username':user.username,
                    'name':user.name,
                    'user_role':user.roles[-1].name}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

class AdminLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        # admin = User.query.filter_by(username=args['username'], role='admin').first()
        admin = User.query.filter_by(username=args['username']).first()
        role = Role.query.get(3)
        if admin and (role in admin.roles):
            if admin and admin.check_password(args['password']):
                access_token = create_access_token(identity=admin.id)
                # return {'access_token': access_token}, 200
                return {'access_token': access_token,
                        'user_id':admin.id,
                        'username':admin.username,
                        'name':admin.name,
                        'user_role':admin.roles[-1].name}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

def adminstats():
    user_count=User.query.count()
    creator_count=User.query.filter(or_(User.status == 'wlc', User.status == 'blc')).count()
    song_count=Song.query.count()
    album_count=Album.query.count()
    return {'user_count':user_count,'creator_count':creator_count,'song_count':song_count,'album_count':album_count}

def allcreators():
    creators=User.query.filter(or_(User.status == 'wlc', User.status == 'blc')).all()
    if creators:
        return [{'user_id':creator.id,'username':creator.username,'name':creator.name,'status':creator.status} for creator in creators] , 200
    return {'msg':"error occured"}, 401

def blacklist_creator(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = "blc"
        db.session.commit()
        return {'message': "Creator blacklisted successfully"}, 200
    return {'message': "Error blacklisting creator"}, 401

def whitelist_creator(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = "wlc"
        db.session.commit()
        return {'message': "Creator whitelisted successfully"}, 200
    return {'message': "Error whitelisting creator"}, 401

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        data=get_jwt_identity()
        print(data)
        return {'message': 'Protected resource'}, 200

def creatorapplication(user_id):
    user=User.query.get(user_id)
    if user:
        user.status="wait"
        db.session.commit()
        return {'message':"application for creator successful"}, 200
    return {'message':"error in application"}, 401

def creatorwaiting():
    wait_users = User.query.filter(User.status == "wait").all()
    return [{'username':user.username,'user_id':user.id} for user in wait_users], 200

def creatorapprove(user_id):
    user=User.query.get(user_id)
    if user:
        user.status="wlc"
        role=Role.query.get(2)
        user.roles.append(role)
        db.session.commit()
        return {'message':"become creator successful"}, 200
    return {'message':"error in approving "}, 401


def creatorreject(user_id):
    user=User.query.get(user_id)
    if user:
        user.status="0"
        db.session.commit()
        return {'message':"application rejected"}, 200
    return {'message':"erro in rejecting application"}, 401


