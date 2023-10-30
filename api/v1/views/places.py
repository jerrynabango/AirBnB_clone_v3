#!/usr/bin/python3
"""Places"""

from flask import jsonify, request, abort
from models.place import Place
from api.v1.views import app_views, storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_city_id(city_id):
    """Provides information about a city in the DB for a given city id."""
    Cit = []
    list = storage.get("City", str(city_id))
    for obj in list.places:
        Cit.append(obj.to_json())
    return jsonify(Cit)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_city(city_id):
    """Adds a new city to the list of cities available"""
    add_place = request.get_json(silent=True)
    if add_place is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", add_place["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in add_place:
        abort(400, 'Missing user_id')
    if "name" not in add_place:
        abort(400, 'Missing name')
    add_place["city_id"] = city_id
    added = Place(**add_place)
    added.save()
    output = jsonify(added.to_json())
    output.status_code = 201
    return output


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def get_place_id(place_id):
    """Performs a GET request to the given place"""
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_place_id(place_id):
    """Performs a POST request to the given place"""
    add_place = request.get_json(silent=True)
    if add_place is None:
        abort(400, 'Not a JSON')
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    for key, value in add_place.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def remove_place_id(place_id):
    """Removes the given place_id from the list of places"""
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})
