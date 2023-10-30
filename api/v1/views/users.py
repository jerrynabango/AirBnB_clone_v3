#!/usr/bin/python3
"""Users"""

from flask import jsonify, request, abort
from . import app_views, User, storage
from hashlib import md5

use = (
    "email",
    "password",
    "first_name",
    "last_name"
    )


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def get_user():
    """Adds a new user """
    if request.method == "GET":
        return jsonify([add.to_dict() for add in storage.all(User).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in use}
            for key in use[:2]:
                if not load.get(key, None):
                    abort(400, description="Missing " + key)
            deleted_user = User(**load)
            storage.new(deleted_user), storage.save()
            return jsonify(deleted_user.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Removes a user from the DataBase and returns the corresponding user object"""
    deleted = storage.get(User, str(user_id))
    if not deleted:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in use[1:]}
            if load.get("password", None):
                ld = load.get("password")
                load.update({"password": md5(bytes(ld, 'utf-8')).hexdigest()})
            [setattr(deleted, key, str(value)) for key, value in load.items()]
            deleted.save()
            return jsonify(deleted.to_dict()), 200
        abort(400, description="Not a JSON")
