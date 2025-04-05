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
def update_one_vehicle(id):
    vehicle = get_vehicle(id)
    if vehicle is None or not request.json:
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

    vehicle_update = update_vehicle(id, request.get_json())

    return jsonify({'vehicle': vehicle_schema.dump(vehicle_update)})

@app.route('/structures/api/v1/vehicles/year', methods=['GET'])
@auth.login_required
def vehicles_by_year_range():
    from_year = request.args.get('from_year')
    to_year = request.args.get('to_year')
    vehicles = get_vehicle_by_year_range(from_year, to_year)
    return jsonify({
        "vehicles":  vehicles_schema.dump(vehicles)
    }), 200

@app.route('/structures/api/v1/vehicles/maker', methods=['GET'])
@auth.login_required
def vehicles_by_maker():
    vehicles = get_vehicle_electric_range_by_make()
    data = [
        {
            "maker": row[0],
            "max_range": row[1],
            "min_range": row[2],
            "avg_range": float(row[3]) if row[3] is not None else None
        }
        for row in vehicles
    ]
    return jsonify({
        "data": data
    }), 200

@app.route('/structures/api/v1/vehicles/city', methods=['GET'])
@auth.login_required
def vehicles_by_city():
    vehicles = get_vehicle_by_city()
    data = [
        {
            "city": row[0],
            "max_range": row[1],
            "min_range": row[2],
            "avg_range": float(row[3]) if row[3] is not None else None
        }
        for row in vehicles
    ]
    return jsonify({
        "data": data
    }), 200

@app.route('/structures/api/v1/vehicles/model', methods=['GET'])
@auth.login_required
def vehicles_by_model():
    vehicles = get_vehicle_electric_range_by_model()
    data = [
        {
            "model": row[0],
            "max_range": row[1],
            "min_range": row[2],
            "avg_range": float(row[3]) if row[3] is not None else None
        }
        for row in vehicles
    ]
    return jsonify({
        "data": data
    }), 200

@app.route('/structures/api/v1/vehicles/country', methods=['GET'])
@auth.login_required
def vehicles_by_country():
    vehicles = get_vehicle_by_country()
    data = [
        {
            "country": row[0],
            "max_range": row[1],
            "min_range": row[2],
            "avg_range": float(row[3]) if row[3] is not None else None
        }
        for row in vehicles
    ]
    return jsonify({
        "data": data
    }), 200

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
