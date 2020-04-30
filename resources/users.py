import models 

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user




users = Blueprint('users', 'users')




@users.route('/', methods=['GET'])
def test_user_resource():
	return "user resource works!"

