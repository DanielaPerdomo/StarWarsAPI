from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #Relacion con Planets (Father)
    planets = db.relationship("Planets", back_populates="user")
    #Relacion con Characters (Father)
    characters = db.relationship("Characters", back_populates="user")

#Esto se debe repetir en cada tabla
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
#Aqui debemos crear nuestras tablas para las relaciones
class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), unique=True, nullable=False)
    populations = db.Column(db.String(50), unique=True, nullable=False)
    rotarion_period = db.Column(db.String(50), unique=True, nullable=False)
    orbital_period = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.String(50), unique=True, nullable=False)
    gravity = db.Column(db.String(50), unique=True, nullable=False)
    terrain = db.Column(db.String(50), unique=True, nullable=False)
    surface_water = db.Column(db.String(50), unique=True, nullable=False)
    climate = db.Column(db.Strin50(50), unique=True, nullable=False)
    #Relacion con User (Child)
    #user = db.relationship("User", back_populates="planets")
    #Relacion con el FavPlanets (Father)
    favPlanets_id = db.Column(db.ForeignKey("favPlanets.id"))
    favPlanets = db.relationship("FavPlanets", back_populates="planets")


    def __repr__(self):
        return '<Planets %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "populations": self.populations,
            "rotarion_period": self.rotarion_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "climate": self.climate,
        }

class FavPlanets(db.Model):
    __tablename__ = 'favPlanets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(50), unique=True, nullable=False)
    species = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.String(50), unique=True, nullable=False)
    mass = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(50), unique=True, nullable=False)
    hair_color = db.Column(db.String(50), unique=True, nullable=False)
    skin_color = db.Column(db.String(50), unique=True, nullable=False)
    homeworld = db.Column(db.Strin50(50), unique=True, nullable=False)
    #Relacion con User (Child)
    #user = db.relationship("User", back_populates="characters")
    #Relacion con FavCharacters (Child)
    favCharacters_id = db.Column(db.ForeignKey("favCharacters.id"))
    favCharacters = db.relationship("FavCharacters", back_populates="characters")



    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "birth_year": self.birth_year,
            "species": self.species,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
        }
    
class FavCharacters(db.Model):
    __tablename__ = 'favCharacters'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
