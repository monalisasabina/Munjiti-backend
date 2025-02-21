from flask import Flask,make_response,request,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User, Pastor, Project, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, cipher

# from flask_jwt_extended import jwt_required, get_jwt_identity

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

        # creating new user
        new_user = User(
            username=username,
            email=email,
            role=role,
        ) 

        new_user.password_hash(password) = password

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


api.add_resource(Users, '/users')       



if __name__ == '__main__':
    app.run(port=5555, debug=True)

