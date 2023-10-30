#!/usr/bin/python3
"""Places reviews into a list of reviews"""

from flask import jsonify, request, abort
from . import app_views, Place, storage, Review, User

ld = (
    "user_id",
    "text"
    )


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"], strict_slashes=False)
def post_place(place_id):
    """Adds a review to the list of reviews for a given place"""
    add_place = storage.get(Place, str(place_id))
    if add_place is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([r.to_dict() for r in add_place.reviews])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in ld}
            for key in ld:
                if not load.get(key, None):
                    abort(400, description="Missing " + key)
                if key == "user_id" and\
                        not storage.get(User, str(load.get("user_id"))):
                    abort(404, description="Not found")
            load.update({"place_id": place_id})
            reviews = Review(**load)
            storage.new(reviews), storage.save()
            return jsonify(reviews.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Removes a review from the review database"""
    deleted_review = storage.get(Review, str(review_id))
    if not deleted_review:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_review.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_review), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            [setattr(deleted_review, key, str(value))
                for key, value in data.items() if key in ld[1:]]
            deleted_review.save()
            return jsonify(deleted_review.to_dict()), 200
        abort(400, description="Not a JSON")
