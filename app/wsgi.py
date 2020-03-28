from werkzeug.wsgi import DispatcherMiddleware
from dash_app import app as dash_app
from flask_app import flask_app

application = DispatcherMiddleware(flask_app, {
    '/dash': dash_app.server
})  