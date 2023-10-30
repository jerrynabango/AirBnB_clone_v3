#!/usr/bin/python3
"""Instances of this module"""

from flask_cors import CORS
from flask import Flask, jsonify
from .views import app_views
from . import models
import os


app = Flask(__name__)

CORS(app, resources=r"/*", origins=["0.0.0.0"])

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(e=None):
    """Clean up the application context and exit."""
    models.storage.close()


@app.errorhandler(404)
def error(e):
    """Checks if the request is not found and returns a 404 error"""
    code = str(e).split()[0]
    result = e.description if "Not found" in e.description else "Not found"
    return jsonify({"error": result}), code


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
