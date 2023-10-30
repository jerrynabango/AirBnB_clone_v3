#!/usr/bin/python3
"""Cities."""

from flask import jsonify, request, abort
from . import app_views, City, State, storage

cty = ("name",)


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def create_city(state_id):
    """Create a NEW City for a specified date"""
    state_server = storage.get(State, str(state_id))
    if state_server is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([list_cit.to_dict()
                        for list_cit in state_server.cities])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            loads = {key: str(value) for key, value in data.items()
                       if key in cty}
            if not loads.get("name", None):
                abort(400, description="Missing name")
            loads.update({"state_id": str(state_id)})
            ct = City(**loads)
            storage.new(ct), storage.save()
            return jsonify(ct.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Removes a city """
    deleted_city = storage.get(City, str(city_id))
    if not deleted_city:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_city.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_city), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data:
            [setattr(deleted_city, key, str(value))
             for key, value in data.items() if key in cty]
            deleted_city.save()
            return jsonify(deleted_city.to_dict()), 200
        abort(400, description="Not a JSON")
