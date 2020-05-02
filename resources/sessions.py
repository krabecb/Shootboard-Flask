import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required




sessions = Blueprint('sessions', 'sessions')



"""HELPER ROUTE -- USER SHOULD ONLY SEE SESSIONS WHEN A CLIENT IS SELECTED"""
@sessions.route('/', methods=['GET'])
@login_required
def sessions_index():
	current_user_session_dicts = [model_to_dict(session) for session in current_user.sessions]

	for session_dict in current_user_session_dicts:
		session_dict['photographer'].pop('password')

	print(current_user_session_dicts)

	return jsonify({
		'data': current_user_session_dicts,
		'message': f"Found {len(current_user_session_dicts)} sessions.",
		'status': 200
	}), 200

@sessions.route('/', methods=['POST'])
@login_required
def create_session():
	payload = request.get_json()
	new_session = models.Session.create(
		title=payload['title'],
		date=payload['date'],
		time=payload['time'],
		location=payload['location'],
		comments=payload['comments'],
		photographer=current_user.id
	)

	session_dict = model_to_dict(new_session)

	print(session_dict)

	session_dict['photographer'].pop('password')

	return jsonify(
		data=session_dict,
		message="Created a session.",
		status=201
	), 201

@sessions.route('/<id>', methods=['DELETE'])
@login_required
def delete_session(id):
	try:
		session_to_delete = models.Session.get_by_id(id)
		if session_to_delete.photographer.id == current_user.id:
			session_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Deleted session with id: {id}.",
				status=200
			), 200
		else:

			return jsonify(
				data={ 'error': '403 Forbidden' },
				message="Photographer's id does not match session's id. Cannot delete.",
				status=403
			), 403
	except models.DoesNotExist:

		return jsonify(
			data={ 'error': '404 not found' },
			message="No existing session with that id.",
			status=404
		), 404

@sessions.route('/<id>', methods=['PUT'])
@login_required
def update_session(id):
	payload = request.get_json()
	session_to_update = models.Session.get_by_id(id)
	if session_to_update.photographer.id == current_user.id:

		if 'title' in payload:
			session_to_update.title = paylod['title']
		if 'date' in payload:
			session_to_update.date = payload['date']
		if 'time' in payload:
			session_to_update.time = payload['time']
		if 'location' in payload:
			session_to_update.location = payload['location']
		if 'comments' in payload:
			session_to_update.comments = payload['comments']

		session_to_update.save()
		update_session_dict = model_to_dict(session_to_update)

		update_session_dict['photographer'].pop('password')

		return jsonify(
			data=update_session_dict,
			message=f"Updated session with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '403 Forbidden' },
			message="Photographer's id does not match session's id. Cannot update.",
			status=403
		), 403

@sessions.route('/<id>', methods=['GET'])
def show_session(id):
	session = models.Session.get_by_id(id)
	if session.photographer.id == current_user.id:
		session_dict = model_to_dict(session)
		session_dict['photographer'].pop('password')

		return jsonify(
			data=session_dict,
			message=f"Found session with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '404 not found' },
			message="You do not have access to this information.",
			status=404
		), 404



