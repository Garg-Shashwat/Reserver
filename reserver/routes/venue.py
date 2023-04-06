from flask import jsonify, request, session, redirect, render_template, url_for, abort

from reserver import app
from reserver.db_methods import query_db, Query


class Venue:
    def __init__(self, capacity, place, location, name=None, id=None) -> None:
        if name:
            self.name = name
        self.capacity = capacity
        self.place = place
        self.location = location
        if id:
            self.id = id


@app.route("/venues", methods=["GET"])
def get_venues():
    if "is_admin" in session and session["is_admin"]:
        query = """
        SELECT venues.id, venues.name,
        GROUP_CONCAT(shows.name) as show_names,
        GROUP_CONCAT(shows.id) as show_ids
        FROM venues
        LEFT JOIN shows ON venues.id = shows.venue_id
        GROUP BY venues.id"""
        venues = query_db(query=query)
        results = [dict(row) for row in venues]
        for venue in results:
            venue["show_names"] = (
                venue["show_names"].split(",") if venue["show_names"] else []
            )
            venue["show_ids"] = (
                venue["show_ids"].split(",") if venue["show_ids"] else []
            )
        return results
    abort(401)


@app.route("/venues/<int:id>", methods=["GET"])
def get_venue(id):
    if "is_admin" in session and session["is_admin"]:
        venues = Query("venues", check_attrs={"id": id}).call_select_query(one=True)
        return dict(venues)
    abort(401)


@app.route("/venues/<int:id>/shows", methods=["GET"])
def get_venue_shows(id):
    if "is_admin" in session and session["is_admin"]:
        shows = Query("shows", check_attrs={"venue_id": id}).call_select_query()
        results = [dict(row) for row in shows]
        return results
    abort(401)


def create_venue(venue: Venue):
    if "is_admin" in session and session["is_admin"]:
        check_venue = Query(
            "venues", check_attrs={"name": venue.name}
        ).call_select_query(one=True)
        if check_venue:
            return "Venue already exists"

        status = Query(
            "venues",
            other_attrs={
                "name": venue.name,
                "capacity": venue.capacity,
                "place": venue.place,
                "location": venue.location,
            },
        ).call_insert_query()
        return status
    abort(401)


def edit_venue(venue: Venue):
    if "is_admin" in session and session["is_admin"]:
        if not venue.id:
            abort(400)

        check_venue = Query("venues", check_attrs={"id": venue.id}).call_select_query(
            one=True
        )
        if not check_venue:
            abort(400)

        status = Query(
            "venues",
            other_attrs={
                "capacity": venue.capacity,
                "place": venue.place,
                "location": venue.location,
            },
            check_attrs={"id": venue.id},
        ).call_update_query()
        return status
    abort(401)


@app.route("/venues/<int:id>", methods=["DELETE"])
def delete_venue(id):
    if "is_admin" in session and session["is_admin"]:
        status = Query("venues", check_attrs={"id": id}).call_delete_query()
        return status
    abort(401)
