#!/usr/bin/python3
"""Stat-Index"""

from . import Amenity, app_views, City, Place, State, storage, Review, User


@app_views.route("/status")
def status():
    """JSON is returned"""
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """Provides all JSON  for stats"""
    all_stats = {}
    set = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User}
    for key, value in set.items():
        all_stats[key] = storage.count(value)
    return all_stats
