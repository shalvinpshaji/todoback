from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todo.config import Config
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config())
api = Api(app)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
from todo import resources