from flask import Flask,make_response,request,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db,ContactMessage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


class MessagesResource(Resource):
    @jwt_required()
    def get(self):

        """Fetch messages for the authenticated user"""
        current_user_email = get_jwt_identity()

        #Fetch messages for the authenticated user
        messages = ContactMessage.query.filter_by(email=current_user_email).all()

        response = [
            {
                'id':msg.id,
                'sender_firstname': msg.sender_firstname,
                'sender_lastname':msg.sender_lastname,
                'email':msg.email,
                'mobile_number':msg.mobile_number,
                'message':msg.message
            }
            for msg in messages
        ]
        return jsonify(response),200

if __name__ == '__main__':
    app.run(port=5555, debug=True)

