from flask import Flask,make_response,request,jsonify,session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User, Pastor, Project, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, ProjectImage, cipher, bcrypt

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)
ADMIN_CODE = os.getenv("ADMIN_CODE")
# print(f"Loaded ADMIN_CODE: {repr(ADMIN_CODE)}")  # Debugging statement

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
                "/pastors",
                "/projects",
                "/projectimages"
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
        
        if not ADMIN_CODE:
            return {'error': 'Server error: ADMIN_CODE not set'},500
        

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

class ChangePassword(Resource):

     def patch(self,id):
      
      user = User.query.get(id)

      if not user:
          return make_response(jsonify({"user":"User not found"}),404)
      
      data = request.get_json()

      old_password = data.get('old_password')
      new_password = data.get('new_password')

      if not old_password or not user.authenticate(old_password):
          return make_response(jsonify({"error":"Incorrect old password"}), 400)
      
      #Ensuring the new password is there and 8 characters long   
      if not new_password or len(new_password) < 8:
          return make_response(jsonify({"error":"Password must be at least 8 characters long"}),400)
      
      user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

      db.session.commit()

      return make_response(jsonify({"message":"Password updated successfully"}),200)
     
api.add_resource(ChangePassword, '/users/<int:id>/change-password', endpoint='user_change_password')     
      


# USER CRUD______________________________________________________________________________________________________________________________________________
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
 
  #Getting each user by ID    
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


  # Updating the user by ID
  def patch(self,id):

        user = User.query.filter(User.id == id).first()

        data =  request.get_json()
        
        if not user:
            return make_response(jsonify({"error":"User not found"}),404)

        try:
            for attr in data:
                setattr(user, attr, data[attr])
   
            db.session.commit()

            user_dict = {
                "username":user.username,
                "email":user.email,
                "role":user.role
            }

            return make_response(jsonify(user_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        

  def delete(self,id):
      
      user = User.query.filter(User.id == id).first()

      if not user:
          return make_response(jsonify({"error":"User not found"}),404)
      
      db.session.delete(user)
      db.session.commit()

      response_dict = {"Message":"User successfully deleted"}

      return make_response(jsonify(response_dict),200)
  

 
api.add_resource(Users_by_ID, '/users/<int:id>')


# Pastor CRUD_____________________________________________________________________________________________________________________________________________
class Pastors(Resource):

    # Fetching all the pastors
    def get(self):

        pastors_list=[]

        for pastor in Pastor.query.all():

            pastor_dict = {
                "id":pastor.id,
                "firstname":pastor.firstname,
                "lastname": pastor.lastname,
                "image":pastor.image,
                "role":pastor.role,
                "description":pastor.description,
                "date_added":pastor.date_added,
            }

            pastors_list.append(pastor_dict)

        return make_response(jsonify(pastors_list),200)
    
    # Adding new pastor
    def post(self):

        try:
            data = request.get_json()

            new_pastor = Pastor(
                firstname = data['firstname'],
                lastname = data['lastname'],
                role = data['role'],
                image = data['image'],
                description = data['description'],
            )

            db.session.add(new_pastor)
            db.session.commit()

            return make_response(new_pastor.to_dict(),201)
        
        except Exception as e:
            return make_response({'errors':['validation errors', str(e)]}, 403)
        


api.add_resource(Pastors, '/pastors')    


class Pastors_by_ID(Resource):

    # Fetching a pastor by ID
    def get(self,id):

        pastor = Pastor.query.filter(Pastor.id == id).first()

        if not pastor:
           return make_response(jsonify({'error':'Pastor  not  found'}),404)
       
        pastor_dict= {
            "id":pastor.id,
            "firstname":pastor.firstname,
            "lastname": pastor.lastname,
            "image": pastor.image,
            "role":pastor.role,
            "description": pastor.description
        }

        return make_response(jsonify(pastor_dict),200)
    

    # Updating the pastor by ID
    def patch(self,id):

        pastor = Pastor.query.filter(Pastor.id == id).first()

        data =  request.get_json()
        
        if not pastor:
            return make_response(jsonify({"error":"Pastor not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(pastor, attr, data[attr])
   
            db.session.commit()

            pastor_dict= {
                "firstname":pastor.firstname,
                "lastname": pastor.lastname,
                "image": pastor.image,
                "role":pastor.role,
                "description": pastor.description
            }

            return make_response(jsonify(pastor_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        
    #Deleting a pastor 
    def delete(self,id):
      
      pastor = Pastor.query.filter(Pastor.id == id).first()

      if not pastor:
          return make_response(jsonify({"error":"Pastor not found"}),404)
      
      db.session.delete(pastor)
      db.session.commit()

      response_dict = {"Message":"Pastor successfully deleted"}

      return make_response(jsonify(response_dict),200)
        

api.add_resource(Pastors_by_ID, '/pastors/<int:id>')   


#Projects CRUD_____________________________________________________________________________________________________________________________________________
class Projects(Resource):
    
    # Fetching all projects
    def get(self):

        projects_list=[]

        for project in Project.query.all():

            project_dict = {
                "id":project.id,
                "name":project.name,
                "description":project.description,
                "date_added":project.date_added,
                "ministries": [ministry.to_dict(rules=('-project',)) for ministry in project.ministries] if project.ministries else [],
                "images": [image.to_dict(rules=('-project',)) for image in project.images] if project.images else []
            }

            # OR
            # project_dict = project.to_dict(rules=('-ministries.project', '-images.project'))

            projects_list.append(project_dict)

        return make_response(jsonify(projects_list),200)
    
    # Adding new project
    def post(self):

        try:
            data = request.get_json()

            new_project = Project(
                name = data['name'],
                description = data['description'] 
            )

            db.session.add(new_project)
            db.session.commit()

            return make_response(new_project.to_dict(rules=('-ministries.project', '-images.project')),201)
            # The rules=('-ministries.project', '-images.project') removes circular relationships that would cause serialization issues.
            # Avoiding TypeError with to_dict().

        except Exception as e:
            return make_response({'errors':['validation errors', str(e)]}, 403)

api.add_resource(Projects, '/projects')


class Project_By_ID(Resource):

    # Fetching a project by ID
    def get(self,id):

        project = Project.query.filter(Project.id == id).first()

        if not project:
           return make_response(jsonify({'error':'Project not found'}),404)
       
        pastor_dict= {
            "id":project.id,
            "name":project.name,
            "description": project.description,
            "ministries": [ministry.to_dict(rules=('-project',)) for ministry in project.ministries] if project.ministries else [],
            "images": [image.to_dict(rules=('-project',)) for image in project.images] if project.images else []   
        }

        return make_response(jsonify(pastor_dict),200)
    
    # Updating the project by ID
    def patch(self,id):

        project = Project.query.filter(Project.id == id).first()

        data =  request.get_json()
        
        if not project:
            return make_response(jsonify({"error":"Project not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(project, attr, data[attr])
   
            db.session.commit()

            project_dict= {
                "name":project.name,
                "description": project.description
            }

            return make_response(jsonify(project_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        

    #Deleting a project 
    def delete(self,id):
      
      project = Project.query.filter(Project.id == id).first()

      if not project:
          return make_response(jsonify({"error":"Project not found"}),404)
      
      db.session.delete(project)
      db.session.commit()

      response_dict = {"Message":"Project successfully deleted"}

      return make_response(jsonify(response_dict),200)
        

api.add_resource(Project_By_ID, '/projects/<int:id>')

# Project Pictures CRUD___________________________________________________________________________________________________________________________________
class ProjectImages(Resource):
 
    # Getting project images
    def get(self):

        projects_image_list=[]

        for project_image in ProjectImage.query.all():

            project_image_dict = {
                "id":project_image.id,
                "image_url":project_image.image_url,
                "project_id":project_image.project_id,
                "project":project_image.project.name if project_image.project else None
            }

            projects_image_list.append(project_image_dict)

        return make_response(jsonify(projects_image_list),200)
    
    # Adding new project image
    def post(self):

        try:
            data = request.get_json()
            print("Received data:", data)

            new_project_image = ProjectImage(
                image_url=data['image_url'],
                project_id=data['project_id']
            )

            db.session.add(new_project_image)
            db.session.commit()

            project_image_dict = new_project_image.to_dict()
            print("Serialized project image:", project_image_dict)  # Debugging

            response =jsonify(project_image_dict)
            response.status_code = 201

            return response 

        except Exception as e:
            print(f"Error details: {str(e)}")
            return {'errors': ['validation errors', str(e)]}, 500
    
api.add_resource(ProjectImages, '/projectimages')

if __name__ == '__main__':
    app.run(port=5557, debug=True)

