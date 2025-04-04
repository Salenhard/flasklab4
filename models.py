from config import db
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cities = db.relationship('City', backref='country', lazy=True, cascade="all, delete")

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    vehicles = db.relationship('Vehicle', backref='city', lazy=True)

class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    models = db.relationship('Model', backref='make', lazy=True)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)
    vehicles = db.relationship('Vehicle', backref='model', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.String(17), primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    electric_range = db.Column(db.Integer, nullable=True)