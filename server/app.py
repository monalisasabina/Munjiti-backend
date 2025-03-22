from flask import Flask,make_response,request,jsonify,session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, joinedload, User, Pastor, Project, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, ProjectImage, cipher, bcrypt

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
                "/projectimages",
                "/ministries",
                "/ministryproject",
                "/notices"
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

class ProjectImages_by_ID(Resource):

    # Fetching project image by ID
    def get(self,id):

        project_image = ProjectImage.query.filter(ProjectImage.id == id).first()

        if not project_image:
           return make_response(jsonify({'error':'Project image not found'}),404)
       
        project_image_dict= {
            "id":project_image.id,
            "image_url":project_image.image_url,
            "project_id":project_image.project_id
        }

        return make_response(jsonify(project_image_dict),200)
    
    # Updating the project image by ID
    def patch(self,id):

        project_image = ProjectImage.query.filter(ProjectImage.id == id).first()

        data =  request.get_json()
        
        if not project_image:
            return make_response(jsonify({"error":"Project image not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(project_image, attr, data[attr])
   
            db.session.commit()

            project_image_dict= {
                "image_url":project_image.image_url,
                "project_id":project_image.project_id
            }

            return make_response(jsonify(project_image_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        
    #Deleting a project image
    def delete(self,id):
      
        project_image = ProjectImage.query.filter(ProjectImage.id == id).first()

        if not project_image:
          return make_response(jsonify({"error":"Project image not found"}),404)
      
        db.session.delete(project_image)
        db.session.commit()

        response_dict = {"Message":"Project image successfully deleted"}

        return make_response(jsonify(response_dict),200)
        
api.add_resource(ProjectImages_by_ID, '/projectimages/<int:id>')


# Ministry CRUD___________________________________________________________________________________________________________________________________________
class MinistryResource(Resource):

    # Getting ministries
    def get(self):

        ministries_list=[]

        for ministry in Ministry.query.options(joinedload(Ministry.projects)).all():

            print(f"Ministry: {ministry.name}, Projects: {ministry.projects}")

            ministry_dict = {
                "id":ministry.id,
                "name":ministry.name,
                "description":ministry.description,
                "projects":[
                    {
                       "id":project.id,
                       "name":project.name
                    }
                    for project in ministry.projects
                ]
            }

            ministries_list.append(ministry_dict)

        return make_response(jsonify(ministries_list),200)
    

    # Adding new ministry image
    def post(self):

        try:
            data = request.get_json()
            print("Received data:", data)

            new_ministry = Ministry(
                name=data['name'],
                description=data['description']
            )

            db.session.add(new_ministry)
            db.session.commit()

            new_ministry_dict = new_ministry.to_dict()

            response =jsonify(new_ministry_dict)
            response.status_code = 201

            return response 

        except Exception as e:
            print(f"Error details: {str(e)}")
            return {'errors': ['validation errors', str(e)]}, 500
    
api.add_resource(MinistryResource, '/ministries')    


class MinistryByID(Resource):

    # Fetching ministry by ID
    def get(self,id):

        ministry = Ministry.query.filter(Ministry.id == id).first()

        if not ministry:
           return make_response(jsonify({'error':'Ministry not found'}),404)
       
        ministry_dict= {
            "id":ministry.id,
            "name":ministry.name,
            "description":ministry.description,
            "projects": [ministry.to_dict(rules=('-ministry',)) for ministry in ministry.projects] if ministry.projects else [],
        }

        return make_response(jsonify(ministry_dict),200)
    

    # Updating a ministry by ID
    def patch(self,id):

        ministry = Ministry.query.filter(Ministry.id == id).first()

        data =  request.get_json()
        
        if not ministry:
            return make_response(jsonify({"error":"Ministry not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(ministry, attr, data[attr])
   
            db.session.commit()

            ministry_dict= {
            "id":ministry.id,
            "name":ministry.name,
            "description":ministry.description,
            }

            return make_response(jsonify(ministry_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        

    #Deleting a ministry
    def delete(self,id):
      
        ministry = Ministry.query.filter(Ministry.id == id).first()

        if not ministry:
          return make_response(jsonify({"error":"Ministry not found"}),404)
      
        db.session.delete(ministry)
        db.session.commit()

        response_dict = {"Message":"Ministry successfully deleted"}

        return make_response(jsonify(response_dict),200)

api.add_resource(MinistryByID, '/ministries/<int:id>')



# MinistryProjects CRUD___________________________________________________________________________________________________________________________________
class MinistyProjectsResource(Resource):

    # Getting ministries
    def get(self):

        ministries_project_list=[]

        for ministry_project_link in MinistryProject.query.all():

            ministry_project_dict = {
                 "ministry_id":ministry_project_link.ministry_id,
                 "project_id":ministry_project_link.project_id

            }

            ministries_project_list.append(ministry_project_dict)

        return make_response(jsonify(ministries_project_list),200)
    

    # Adding ministry_project link
    def post(self):

        try:
            data = request.get_json()
            print("Received data:", data)

            new_ministry_project_link = MinistryProject(
                ministry_id=data['ministry_id'],
                project_id=data['project_id']
            )

            db.session.add(new_ministry_project_link)
            db.session.commit()

            ministry_project_dict = new_ministry_project_link.to_dict()
            
            response =jsonify(ministry_project_dict)
            response.status_code = 201

            return response 

        except Exception as e:
            print(f"Error details: {str(e)}")
            return {'errors': ['validation errors', str(e)]}, 500
    
api.add_resource(MinistyProjectsResource, '/ministryproject')  


class MinistryProjectByID(Resource):

    # Fetching ministry_project by ID
    def get(self,id):

        ministry_project = MinistryProject.query.filter(MinistryProject.id == id).first()

        if not ministry_project:
           return make_response(jsonify({'error':'Ministry_Project link not found'}),404)
       
        ministry_project_dict= {
            "id":ministry_project.id,
            "ministry_id":ministry_project.ministry_id,
            "project_id":ministry_project.project_id
        }

        return make_response(jsonify(ministry_project_dict),200)
    

    # Updating a ministry_project by ID
    def patch(self,id):

        ministry_project = MinistryProject.query.filter(MinistryProject.id == id).first()

        data =  request.get_json()
        
        if not ministry_project:
            return make_response(jsonify({"error":"Ministry_Project link not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(ministry_project, attr, data[attr])
   
            db.session.commit()

            ministry_project_dict= {
                "id":ministry_project.id,
                "ministry_id":ministry_project.ministry_id,
                "project_id":ministry_project.project_id
            }

            return make_response(jsonify(ministry_project_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        

    #Deleting a ministry_project_link
    def delete(self,id):
      
        ministry_project = MinistryProject.query.filter(MinistryProject.id == id).first()

        if not ministry_project:
          return make_response(jsonify({"error":"Ministry_Project link not found"}),404)
      
        db.session.delete(ministry_project)
        db.session.commit()

        response_dict = {"Message":"Ministry_Project link successfully deleted"}

        return make_response(jsonify(response_dict),200)

api.add_resource(MinistryProjectByID, '/ministryproject/<int:id>')


# Notices CRUD___________________________________________________________________________________________________________________________________________
class NoticeResource(Resource):

    # Fetching notices
    def get(self):

        notices_list=[]

        for notice in Notice.query.all():

            notice_dict = {
                "id":notice.id,
                "title":notice.title,
                "notice_text":notice.notice_text,
                "image":notice.image,
                "date_added":notice.date_added
        
            }

            notices_list.append(notice_dict)

        return make_response(jsonify(notices_list),200)
    

    # Adding new ministry image
    def post(self):

        try:
            data = request.get_json()
            print("Received data:", data)

            new_notice = Notice(
                title=data['title'],
                notice_text=data['notice_text'],
                image=data['image'],
            )

            db.session.add(new_notice)
            db.session.commit()

            new_notice_dict = new_notice.to_dict()

            response =jsonify(new_notice_dict)
            response.status_code = 201

            return response 

        except Exception as e:
            print(f"Error details: {str(e)}")
            return {'errors': ['validation errors', str(e)]}, 500
        

api.add_resource(NoticeResource, '/notices')

class NoticeById(Resource):

    # Fetching notice by ID
    def get(self,id):

        notice = Notice.query.filter(Notice.id == id).first()

        if not notice:
           return make_response(jsonify({'error':'Notice not found'}),404)
        
        notice_dict = {
                "id":notice.id,
                "title":notice.title,
                "notice_text":notice.notice_text,
                "image":notice.image,
                "date_added":notice.date_added
        }
       
        return make_response(jsonify(notice_dict),200)


    # Updating a notice by ID
    def patch(self,id):

        notice = Notice.query.filter(Notice.id == id).first()

        data =  request.get_json()
        
        if not notice:
            return make_response(jsonify({"error":"Notice not found"}),404)
        
        if not data:
            return make_response(jsonify({"error": "Invalid JSON format"}),400)

        try:
            for attr in data:
                setattr(notice, attr, data[attr])
   
            db.session.commit()

            notice_dict = {
                "title":notice.title,
                "notice_text":notice.notice_text,
                "image":notice.image,   
            }

            return make_response(jsonify(notice_dict), 200)

        except Exception as e:
            return make_response(jsonify({"error":"validation errors", "details": str(e)}),400)
        

    #Deleting a notice
    def delete(self,id):
      
        notice = Notice.query.filter(Notice.id == id).first()

        if not notice:
          return make_response(jsonify({"error":"Notice not found"}),404)
      
        db.session.delete(notice)
        db.session.commit()

        response_dict = {"Message":"Notice successfully deleted"}

        return make_response(jsonify(response_dict),200)
        

api.add_resource(NoticeById, '/notices/<int:id>')    

if __name__ == '__main__':
    app.run(port=5555, debug=True)

