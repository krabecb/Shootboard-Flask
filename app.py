"""IMPORTS"""
from flask import Flask, jsonify

from resources.users import users

from resources.clients import clients

from resources.sessions import sessions

import models

from flask_cors import CORS

from flask_login import LoginManager




DEBUG=True
PORT=8000


app=Flask(__name__)


app.secret_key = "Secret string."

"""USER OBJECT LOADED WHEN USER LOGGED IN"""
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print("Loading the following user:")
		user = models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return None

"""SEND BACK JSON"""
@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
			'error': 'User not logged in'
		},
		message="You must be logged in to do that.",
		status=401
	), 401

"""CORS"""
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(clients, origins=['http://localhost:3000'], supports_credentials=True)
CORS(sessions, origins=['http://localhost:3000'], supports_credentials=True)




app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(clients, url_prefix='/api/clients')
app.register_blueprint(sessions, url_prefix='/api/sessions')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)