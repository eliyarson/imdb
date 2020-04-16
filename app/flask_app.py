#flask_app.py
from flask import Flask, render_template

flask_app = Flask(__name__)

#home page
@flask_app.route('/')
def index():
    return render_template('simple.html')

if __name__=='__main__':
    flask_app.run(debug=True)