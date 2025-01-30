from flask import Flask,make_response,request
from flask_migrate import Migrate
from flask_restful import Api

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

