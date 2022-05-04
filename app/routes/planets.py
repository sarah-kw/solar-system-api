from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

# planet_list = [
#     Planet(1, "Mercury", "The red planet", 57900000),
#     Planet(2, "Venus", "Many many clouds", 108200000),
#     Planet(3, "Earth", "If you don't live here, let's chat", 149600000)
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

def handle_id_requests(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"msg":f"Planet ID '{id}' is invalid. Requires int."}, 400))
    
    id_returned_planet = Planet.query.get(id)
    if not id_returned_planet:
        abort(make_response({"msg": f"Planet ID '{id}' does not exist"}, 404))
    
    return id_returned_planet

def handle_full_planet_request_body(request):
    request_body = request.get_json()
    expected_elements = {"planet_name":str, "description":str, "dist_from_star_km":int}
    if all(element in request_body for element in expected_elements):
        if all(type(request_body[element]) == expected_elements[element] for element in expected_elements):
            return request_body

    abort(make_response({"msg": f"Planet must have attributes {expected_elements}"}, 400))


@planets_bp.route("", methods=["GET"])
def get_planets():
    planet_response = []

    planet_query = request.args
    if 'name' in planet_query:
        planet_list = Planet.query.filter_by(planet_name=planet_query['name'])
    else:
        planet_list = Planet.query.all()

    for planet in planet_list:
        planet_response.append(planet.make_dict())
    
    return jsonify(planet_response)

@planets_bp.route("/<id>", methods=["GET"])
def get_one_planet(id):
    selected_planet = handle_id_requests(id)
    planet_return = selected_planet.make_dict()
    return jsonify(planet_return), 200

@planets_bp.route("", methods=["POST"])
def add_planet_to_db():
    request_body = handle_full_planet_request_body(request)
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

@planets_bp.route("/<id>", methods=["PUT"])
def put_replace_planet_record(id):
    selected_planet = handle_id_requests(id)
    request_body = handle_full_planet_request_body(request)

    selected_planet.planet_name = request_body["planet_name"]
    selected_planet.description = request_body["description"]
    selected_planet. dist_from_star_km = request_body["dist_from_star_km"]
    
    db.session.commit()

    return make_response(f"Planet #{id} successfully updated", 200)

@planets_bp.route("/<id>", methods=["DELETE"])
def delete_planet_record(id):
    selected_planet = handle_id_requests(id)
    db.session.delete(selected_planet)
    db.session.commit()

    return make_response(f"Planet #{id} successfully deleted", 200)