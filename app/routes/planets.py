from flask import Blueprint, jsonify, abort, make_response

# class Planet:
#     def __init__(self, id, name, description, dist_from_star_km):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.dist_from_star_km = dist_from_star_km
    
#     def make_dict(self):
#         planet_dict = {
#             "id": self.id,
#             "name": self.name,
#             "description": self.description,
#             "dist_from_star_km": self.dist_from_star_km
#             }
#         return planet_dict


# planet_list = [
#     Planet(1, "Mercury", "The red planet", 57900000),
#     Planet(2, "Venus", "Many many clouds", 108200000),
#     Planet(3, "Earth", "If you don't live here, let's chat", 149600000)
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_planets():
    planet_response = []
    for planet in planet_list:
        planet_response.append(planet.make_dict())
    return jsonify(planet_response)


def handle_GET_id_requests(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"msg":f"Planet ID '{id}' is invalid. Requires int."}, 400))
    return id

@planets_bp.route("/<id>", methods=["GET"])
def get_one_planet(id):
    id = handle_GET_id_requests(id)
    
    planet_return = None
    for planet in planet_list:
        if planet.id == id:
            planet_return = planet.make_dict()
    if not planet_return:
        return {"msg": f"Planet ID '{id}' does not exist"}, 404
    return jsonify(planet_return), 200
