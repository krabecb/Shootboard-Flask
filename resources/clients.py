import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required




clients = Blueprint('clients', 'clients')




@clients.route('/', methods=['GET'])
@login_required
def clients_index():
	current_user_client_dicts = [model_to_dict(client) for client in current_user.clients]

	for client_dict in current_user_client_dicts:
		client_dict['photographer'].pop('password')

	print(current_user_client_dicts)

	return jsonify({
		'data': current_user_client_dicts,
		'message': f"Found {len(current_user_client_dicts)} clients.",
		'status': 200
	}), 200

@clients.route('/', methods=['POST'])
@login_required
def create_client():
	payload = request.get_json()
	new_client = models.Client.create(
		first_name=payload['first_name'],
		last_name=payload['last_name'],
		date_of_birth=payload['date_of_birth'],
		location=payload['location'],
		photographer=current_user.id
	)

	client_dict = model_to_dict(new_client)

	print(client_dict)

	client_dict['photographer'].pop('password')

	return jsonify(
		data=client_dict,
		message="Created a client.",
		status=201
	), 201

@clients.route('/<id>', methods=['DELETE'])
@login_required
def delete_client(id):
	try:
		client_to_delete = models.Client.get_by_id(id)
		if client_to_delete.photographer.id == current_user.id:
			client_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Deleted client with id: {id}.",
				status=200
			), 200
		else:

			return jsonify(
				data={ 'error': '403 Forbidden' },
				message="Photographer's id does not match client's id. Cannot delete.",
				status=403
			), 403
	except models.DoesNotExist:

		return jsonify(
			data={ 'error': '404 not found' },
			message="No existing client with that id.",
			status=404
		), 404

@clients.route('/<id>', methods=['PUT'])
@login_required
def update_client(id):
	payload = request.get_json()
	client_to_update = models.Client.get_by_id(id)
	if client_to_update.photographer.id == current_user.id:

		if 'first_name' in payload:
			client_to_update.first_name = payload['first_name']
		if 'last_name' in payload:
			client_to_update.last_name = payload['last_name']
		if 'date_of_birth' in payload:
			client_to_update.date_of_birth = payload['date_of_birth']
		if 'location' in payload:
			client_to_update.location = payload['date_of_birth']

		client_to_update.save()
		updated_client_dict = model_to_dict(client_to_update)

		updated_client_dict['photographer'].pop('password')

		return jsonify(
			data=updated_client_dict,
			message=f"Updated client with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '403 Forbidden' },
			message="Photographer's id does not match client's id. Cannot update.",
			status=403
		), 403

@clients.route('/<id>', methods=['GET'])
def show_client(id):
	client = models.Client.get_by_id(id)
	if client.photographer.id == current_user.id:
		client_dict = model_to_dict(client)
		client_dict['photographer'].pop('password')
		
		return jsonify(
			data=client_dict,
			message=f"Found client with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '404 not found' },
			message="You do not have access to this information.",
			status=404
		), 404