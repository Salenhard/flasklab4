from config import db
from models import Country, City, Vehicle, Make, Model
from structures.serializers import vehicle_schema, vehicles_schema
from sqlalchemy import func
from uuid import uuid4

def get_all_vehicles():
    query = Vehicle.query.all()

    return query


def get_vehicle(building_id):
    query = Vehicle.query.filter(Vehicle.id == building_id).one_or_none()
    return query

def get_vehicle_electric_range_by_model():
    query = (
        db.session.query(
            Model.name.label("Модель"),
            func.max(Vehicle.electric_range).label("Максимальный запас хода"),
            func.min(Vehicle.electric_range).label("Минимальный запас хода"),
            func.avg(Vehicle.electric_range).label("Средний запас хода")
        )
        .select_from(Vehicle)
        .join(Model)
        .group_by(Model.name)
    )
    return query.all()

def get_vehicle_electric_range_by_make():
    query = (
        db.session.query(
            Make.name.label("Производитель"),
            func.max(Vehicle.electric_range).label("Максимальный запас хода"),
            func.min(Vehicle.electric_range).label("Минимальный запас хода"),
            func.avg(Vehicle.electric_range).label("Средний запас хода")
        )
        .select_from(Vehicle)
        .join(Model)
        .join(Make)
        .group_by(Make.name)
    )
    return query.all()

def get_vehicle_by_year_range(from_year, to_year):
    return Vehicle.query.filter(Vehicle.model_year.between(from_year, to_year)).all()

def get_vehicle_by_city():
    query = (
        db.session.query(
            City.name.label("Город"),
            func.max(Vehicle.electric_range).label("Максимальный запас хода"),
            func.min(Vehicle.electric_range).label("Минимальный запас хода"),
            func.avg(Vehicle.electric_range).label("Средний запас хода")
        )
        .select_from(Vehicle)
        .join(City)
        .group_by(City.name)
    )
    return query.all()

def get_vehicle_by_country():
    query = (
        db.session.query(
            Country.name.label("Страна"),
            func.max(Vehicle.electric_range).label("Максимальный запас хода"),
            func.min(Vehicle.electric_range).label("Минимальный запас хода"),
            func.avg(Vehicle.electric_range).label("Средний запас хода")
        )
        .select_from(Vehicle)
        .join(City)
        .join(Country)
        .group_by(Country.name)
    )
    return query.all()

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
