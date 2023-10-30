#!/usr/bin/python3
"""States"""

from flask import jsonify, request, abort
from . import app_views, State, storage

stat = ("name",)


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def get_states():
    """Provides a list of states available"""
    if request.method == "GET":
        return jsonify([stat.to_dict()
                        for stat in storage.all(State).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            payload = {key: str(value) for key, value in data.items()
                       if key in stat}
            if not payload.get("name", None):
                abort(400, description="Missing name")
            created_state = State(**payload)
            storage.new(created_state), storage.save()
            return jsonify(created_state.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/states/<state_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_state_id(state_id):
    """Provides information about the state for the given state id"""
    list_state = storage.get(State, str(state_id))
    if not list_state:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(list_state.to_dict())
    elif request.method == "DELETE":
        storage.delete(list_state), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data:
            [setattr(list_state, key, str(value))
             for key, value in data.items() if key in stat]
            list_state.save()
            return jsonify(list_state.to_dict()), 200
        abort(400, description="Not a JSON")
