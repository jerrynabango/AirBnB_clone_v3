#!/usr/bin/python3
"""Place_Amenity"""

from flask import jsonify, request, abort
from . import Amenity, app_views, Place, storage
import os


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_amenity_place(place_id):
    """Provides information about a place and amenities"""
    amenity_place = storage.get(Place, str(place_id))
    if amenity_place is None:
        abort(404, description="Not found")
    return jsonify([list.to_dict() for list in amenity_place.ament_place])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"], strict_slashes=False)
def delete_amenity_place(amenity_id, place_id):
    """Removes place_amenity from the place"""
    amenity_place = storage.get(Place, str(place_id))
    place_amenity = storage.get(Amenity, str(amenity_id))
    if amenity_place is None or place_amenity is None:
        abort(404, description="Not found")
    server = os.getenv("HBNB_TYPE_STORAGE", None)
    if request.method == "DELETE":
        if place_amenity not in amenity_place.ament_place:
            abort(404, description="Not found")
        if server == "db":
            amenity_place.ament_place.remove(place_amenity)
        else:
            amenity_place.amenit_id.remove(place_amenity.id)
        storage.save()
        return jsonify({})
    else:
        if place_amenity in amenity_place.ament_place:
            return jsonify({})
        if server == "db":
            amenity_place.ament_place.append(place_amenity)
        else:
            amenity_place.amenit_id.append(place_amenity.id)
        storage.save()
        return jsonify(place_amenity.to_dict()), 201
