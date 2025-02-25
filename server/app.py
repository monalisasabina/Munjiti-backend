from flask import Flask,make_response,request,jsonify,session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User, Pastor, Project, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, cipher

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), ".gitignore", ".env")
load_dotenv(dotenv_path, override=True)
ADMIN_CODE = os.getenv("ADMIN_CODE")
# print(f"Loaded ADMIN_CODE: {repr(ADMIN_CODE)}")  # Debugging statement

from models import db,ContactMessage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app)


# HOME PAGE
class Home(Resource):
    def get(self):
        return{
            "message":"Welcome to the Munjiti Church API",
            "Api_version":"v1",
            "available_endpoints":[
                "/users",
                "/pastors"
            ]
        },200
api.add_resource(Home,'/')


# Authentication process
# Signing up
class Signup(Resource):

    def post(self):

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')
        code = data.get('code')

        if not username or not password or not email or not role:
            return {'error': 'Username, email , password and role required'}, 400

        #checking if username exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'error':'Username already taken'}, 400 

        #checking if email exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return {'error':'Email; already taken'}, 400
        
        # checking code
        if code != ADMIN_CODE:
          return {'error': 'Invalid admin code'},403
        

        # creating new user
        new_user = User(
            username=username,
            email=email,
            role=role,
        ) 

        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

    
        new_user_data = {
            "id":new_user.id,
            "username":new_user.username,
            "role":new_user.role
        }

        return {
            'message':'User created successfully',
            'user':new_user_data
        },201
    
api.add_resource(Signup, '/signup', endpoint='signup')    

# Logging in
class Login(Resource):

    def post(self):

        data =  request.get_json()

        if not data:
            return {'error':'Invalid JSON format'},400
        
        username =  data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        user = User.query.filter(User.username == username).first()

        if not user:
            return {'error':'User not found'},401
        
        if not user.authenticate(password):
            return {'error':'Invalid credentials'},401
        
        # Store user in session
        session['user_id'] = user.id

        return {
            'message':'Logged in successfully',
            'user':{
                'name':user.username,
                'email':user.email,
                'role':user.role
            }
        },200

api.add_resource(Login, '/login', endpoint='login')


# Staying logged in
class CheckSession(Resource):
    
    def get(self):
        if 'user_id' in session:
            user = User.query.get(session['user_id'])

            if user:
                return {'message':'User authentication','user':{'id':user.id, 'name':user.username}
                    },200
            else:
                session.pop('user_id', None)
                return{'error':'User not found'},404
            
        return{'error':'Session not found'},401


api.add_resource(CheckSession, '/check_session', endpoint='check_session')

#Logout
class Logout(Resource):

    def delete(self):

        session.pop('user_id', None)
        return{},204

api.add_resource(Logout, '/logout', endpoint='logout')   


 
# USER CRUD
class Users(Resource):
    
    def get(self):

        users_list=[]

        for user in User.query.all():

            user_dict = {
                "id":user.id,
                "username":user.username,
                "role":user.role
            }

            users_list.append(user_dict)

        return make_response(jsonify(users_list),200)

    
    def post(self):

        try:
            data = request.get_json()

            new_user = User(
                username = data['username'],
                role = data['role'],
                email = data['email']
            )

            db.session.add(new_user)
            db.session.commit()

            return make_response(new_user.to_dict(),201)
        
        except Exception as e:
            return make_response({'errors':['validation errors', str(e)]}, 403)


api.add_resource(Users, '/users', endpoint='users')      


# Users by ID
class Users_by_ID(Resource):

  def get(self,id):

    user = User.query.filter(User.id == id).first()

    if not user:
      return make_response(jsonify({'error':'User  not  found'}),404)
       
    user_dict= {
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.role
        }
    return make_response(jsonify(user_dict),200)
        

api.add_resource(Users_by_ID, '/users/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

