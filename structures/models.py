from config import db
from models import Country, City, Vehicle, Make
from structures.serializers import vehicle_schema, vehicles_schema
from uuid import uuid4

def get_all_vehicles():
    query = Vehicle.query.all()

    return query


def get_vehicle(building_id):
    query = Vehicle.query.filter(Vehicle.id == building_id).one_or_none()
    return query


def insert_vehicle(vehicle):
    vehicle_id = str(uuid4())[:17]
    vehicle["id"] = vehicle_id
    item = vehicle_schema.load(vehicle, session=db.session)
    db.session.add(item)
    db.session.commit()
    return ((Vehicle.query
             .filter(Vehicle.id == vehicle_id))
            .one_or_none())


def update_vehicle(id, data):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        raise ValueError("Vehicle not found")

    if 'model_id' in data:
        if not isinstance(data['model_id'], int):
            raise ValueError("model_id must be an integer")
        if not Make.query.get(data['model_id']):
            raise ValueError("Invalid model_id")
    if 'city_id' in data:
        if not isinstance(data['city_id'], int):
            raise ValueError("city_id must be an integer")
        if not City.query.get(data['city_id']):
            raise ValueError("Invalid city_id")
    if 'model_year' in data and not isinstance(data['model_year'], int):
        raise ValueError("model_year must be an integer")
    if 'height' in data and not isinstance(data['electric_range'], int):
        raise ValueError("electric_range must be an integer")

    for key, value in data.items():
        if hasattr(vehicle, key):
            setattr(vehicle, key, value)

    try:
        db.session.commit()
        return vehicle
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error updating vehicle: {str(e)}")


def delete_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        raise ValueError("Vehicle not found")

    try:
        db.session.delete(vehicle)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error deleting vehicle: {str(e)}")
