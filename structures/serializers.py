from models import Vehicle, Make, Country, City
from config import ma, db


class MakeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Make


class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Country


class CitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = City

    country = ma.Nested(CountrySchema())


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        sqla_session = db.session

    model_id = ma.auto_field()
    city_id = ma.auto_field()


vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
