from app import app, auth
from flask import jsonify, abort, make_response, request
from structures.models import *
from structures.serializers import vehicles_schema, vehicle_schema

@app.route('/structures/api/v1/vehicles', methods=['GET'])
@auth.login_required
def get_buildings():
    buildings = get_all_vehicles()

    return jsonify({"vehicles": vehicles_schema.dump(buildings)})


@app.route('/structures/api/v1/vehicles/<string:id>', methods=['GET'])
@auth.login_required
def get_one_building(id):
    building = get_vehicle(id)
    if building is None:
        abort(404)
    return jsonify({"vehicle": vehicle_schema.dump(building)})


@app.route('/structures/api/v1/vehicles', methods=['POST'])
@auth.login_required
def create_building():

    if (not request.json
            or 'model_id' not in request.json
            or 'city_id' not in request.json):
        abort(400)

    new_vehicle = request.get_json()

    if 'electric_range' not in request.json:
        new_vehicle['electric_range'] = 0
    if 'model_year' not in request.json:
        new_vehicle['model_year'] = 2000
    try:
        vehicle_new = insert_vehicle(new_vehicle)
    except Exception as e:
        abort(400, e.args)

    return jsonify({'vehicle': vehicle_schema.dump(vehicle_new)}), 201


@app.route('/structures/api/v1/vehicles/<string:id>', methods=['PUT'])
@auth.login_required
def update_one_building(id):
    building = get_vehicle(id)
    if building is None or not request.json:
        abort(404)
    if ('model_id' in request.json and
            type(request.json['model_id']) is not int):
        abort(400)
    if 'city_id' in request.json and type(request.json['city_id']) is not int:
        abort(400)
    if 'model_year' in request.json and type(request.json['model_year']) is not int:
        abort(400)
    if 'electric_range' in request.json and type(request.json['electric_range']) is not int:
        abort(400)

    building_update = update_vehicle(id, request.get_json())

    return jsonify({'building': vehicle_schema.dump(building_update)})


@app.route('/structures/api/v1/vehicles/<string:id>', methods=['DELETE'])
@auth.login_required
def delete_one_building(id):
    try:
        delete_vehicle(id)
    except Exception as e:
        abort(400, e.args)
    return make_response(jsonify({'message': 'No content'}), 204)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
