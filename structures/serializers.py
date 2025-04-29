from models import Vehicle, Make, Country, City
from config import ma, db
from flask import url_for

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

    city = ma.Nested(CitySchema)
    model = ma.Nested(MakeSchema)

    self = ma.Hyperlinks(
        ma.URLFor('get_one_vehicle', values={'vehicle_id': '<id>'})
    )

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
