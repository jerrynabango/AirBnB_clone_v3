#!/usr/bin/python3
"""Amenities"""

from flask import jsonify, request, abort
from . import Amenity, app_views, storage

amenities = ("name",)


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def create_amenit():
    """Create New amenities"""
    if request.method == "GET":
        return jsonify([stored_amenit.to_dict()
                        for stored_amenit in storage.all(Amenity).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            payload = {key: str(value) for key, value in data.items()
                       if key in amenities}
            if not payload.get("name", None):
                abort(400, description="Missing name")
            amenit = Amenity(**payload)
            storage.new(amenit), storage.save()
            return jsonify(amenit.to_dict()), 201
        abort(400, description="Not stored_amenit JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Removes an amenity from the backend storage."""
    amenity_storage = storage.get(Amenity, str(amenity_id))
    if not amenity_storage:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(amenity_storage.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenity_storage), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            [setattr(amenity_storage, key, str(value))
             for key, value in data.items() if key in amenities]
            amenity_storage.save()
            return jsonify(amenity_storage.to_dict()), 200
        abort(400, description="Not stored_amenit JSON")
