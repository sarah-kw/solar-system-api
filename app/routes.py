from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, dist_from_star_km):
        self.id = id
        self.name = name
        self.description = description
        self.dist_from_star_km = dist_from_star_km


planet_list = [
    Planet(1, "Mercury", "The red planet", 57900000),
    Planet(2, "Venus", "Many many clouds", 108200000),
    Planet(3, "Earth", "If you don't live here, let's chat", 149600000)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_planets():
    planet_response = []
    for planet in planet_list:
        planet_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "dist_from_star_km": planet.dist_from_star_km
            }
        )
    return jsonify(planet_response)
