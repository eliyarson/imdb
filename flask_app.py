#flask_app.py
from flask import Flask

flask_app = Flask(__name__)

#home page
@flask_app.route('/')
def index() :
    return "Welcome to my Internet Movies DashBoard "

