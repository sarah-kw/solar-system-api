from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

# planet_list = [
#     Planet(1, "Mercury", "The red planet", 57900000),
#     Planet(2, "Venus", "Many many clouds", 108200000),
#     Planet(3, "Earth", "If you don't live here, let's chat", 149600000)
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_planets():
    planet_response = []
    planet_list = Planet.query.all()
    for planet in planet_list:
        planet_response.append(planet.make_dict())
    return jsonify(planet_response)


def handle_GET_id_requests(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"msg":f"Planet ID '{id}' is invalid. Requires int."}, 400))
    return id

# @planets_bp.route("/<id>", methods=["GET"])
# def get_one_planet(id):
#     id = handle_GET_id_requests(id)
    
#     planet_return = None
#     for planet in planet_list:
#         if planet.id == id:
#             planet_return = planet.make_dict()
#     if not planet_return:
#         return {"msg": f"Planet ID '{id}' does not exist"}, 404
#     return jsonify(planet_return), 200

@planets_bp.route("", methods=["POST"])
def add_planet_to_db():
    request_body = request.get_json()
    new_planet = Planet(
        planet_name = request_body["planet_name"],
        description = request_body["description"],
        dist_from_star_km = request_body["dist_from_star_km"]
    )

    db.session.add(new_planet)
    db.session.commit()

    response = make_response(
        f"New planet {new_planet.planet_name} successfully created", 
        201
        )
    return response