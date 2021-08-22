from flask import Flask
from flask_restplus import Api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

