#!/usr/bin/python3
"""Instances of this module"""

from flask_cors import CORS
from flask import Flask, jsonify
from .views import app_views
from os import getenv
from . import models


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """Clean up the application context and exit."""
    models.storage.close()


@app.errorhandler(404)
def error(e):
    """Checks if the request is not found and returns a 404 error"""
    error = str(e).split()[0]
    output = e.description if "Not found" in e.description else "Not found"
    return jsonify({"error": output}), error


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
