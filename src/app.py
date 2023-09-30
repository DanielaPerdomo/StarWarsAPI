"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, FavPlanets, FavCharacters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#Desde aqui creamos los Endpoints del Proyecto de StarWars
#Metodo Get Listar todos los registros de people en la base de datos
@app.route('/people', methods=['GET'])
def all_character():
    character = Characters.query.all()
    arr_character = list(map(lambda people: people.serialize(), character))
    print(arr_character)
    return jsonify(arr_character), 200

#Metodo Get Listar la información de una sola people
@app.route('/people/<int:people_id>', methods=['GET'])
def one_character(people_id):
    one_people = Characters.query.get(people_id)
    print(one_people)
    return jsonify(one_people.serialize()), 200

#Metodo Get Listar todos los registros de planetas en la base de datos
@app.route('/planets', methods=['GET'])
def all_planets():
    planets = Planets.query.all()
    arr_planets = list(map(lambda planets: planets.serialize(), planets))
    print(arr_planets)
    return jsonify(arr_planets), 200

#Metodo Get Listar la información de un solo planeta
@app.route('/planets/<int:planet_id>', methods=['GET'])
def one_planet(planet_id):
    one_world = Planets.query.get(planet_id)
    print(one_world)
    return jsonify(one_world.serialize()), 200

#Metodo POST para crear los usuarios del blog
@app.route('/create/user', methods=['POST'])
def create_user():
    body = request.json
    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    user = User(
        name = name,
        email = email,
        password = password
    )
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        }), 500
    return jsonify({}), 201

#Metodo GET Listar todos los usuarios del blog
@app.route('/users', methods=['GET'])
def all_users():
    user = User.query.all()
    arr_user = list(map(lambda person: person.serialize(), user))
    
    return jsonify(arr_user), 200

#Metodo GET Listar todos los favoritos que pertenecen al usuario actual
@app.route('/users/favorites/<int:users_id>', methods=['GET'])
def user_favotites(users_id):

    # Localizar el usuario sus favoritos

    # PLANET FAVORITO
    planet_favorite = FavPlanets.query.filter_by(user_id = users_id)
    planet = [planets.serialize() for planets in planet_favorite]

    # CHARACTERS FAVORITO
    character_favorite = FavCharacters.query.filter_by(user_id = users_id)
    character = [character.serialize() for character in character_favorite]

    return jsonify("Favorites", planet, character), 200



#Metodo POST Añade un nuevo planet favorito al usuario actual con el planet id = planet_id

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    select_planet= Planets.query.get(planet_id)
    body =  request.json
    id_user = body.get("id_user")
    actual_user = User.query.get(id_user)

    favorite_planet = FavPlanets(
        user = actual_user,
        planets = select_planet
    )

    try:
        db.session.add(favorite_planet)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

#Metodo POST Añade una nueva people favorita al usuario actual con el people.id = people_id

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_character(characters_id):
    select_character = Characters.query.get(characters_id)
    body = request.json
    id_user = body.get("id_user")
    actual_user = User. query.get(id_user)

    fav_character = FavCharacters(
        user = actual_user,
        characters = select_character
    )
    
    try:
        db.session.add(fav_character)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200


#Metodo DELETE Elimina un planet favorito con el id = planet_id

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    delete_planet = FavPlanets.query.get(planet_id)

    try:
        db.session.delete(delete_planet)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200

#Metodo DELETE  Elimina una people favorita con el id = people_id

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_character(characters_id):
    delete_character = FavCharacters.query.get(characters_id)

    try:
        db.session.delete(delete_character)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ERROR INTERNO",
            "error": error.args
        })
    return jsonify({}), 200
"""
@app.route('/todos', methods=['POST'])
def add_new_todo():
    request_body = request.json
    todos.append(request_body)
    json_body = jsonify(todos)
    return json_body

@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    todos.pop(position - 1)
    json_todos = jsonify(todos)
    return json_todos
"""
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
