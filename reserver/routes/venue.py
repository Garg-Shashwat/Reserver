from flask import jsonify, request, session, redirect, render_template, url_for, abort

from reserver import app
from reserver.db_methods import query_db, Query


@app.route("/venues", methods=["GET"])
def get_venues():
    if "is_admin" in session and session["is_admin"]:
        query = """
        SELECT venues.id, venues.name,
        GROUP_CONCAT(shows.name) as show_names
        FROM venues
        LEFT JOIN shows ON venues.id = shows.venue_id
        GROUP BY venues.id"""
        venues = query_db(query=query)
        results = [dict(row) for row in venues]
        print(results)
        return results
    abort(401)


@app.route("/venues/<int:id>", methods=["GET"])
def get_venue(id):
    if "is_admin" in session and session["is_admin"]:
        venues = Query("venues", check_attrs={"id": id}).call_select_query(one=True)
        return jsonify(dict(venues))
    abort(401)


@app.route("/venues/<int:id>/shows", methods=["GET"])
def get_venue_shows(id):
    if "is_admin" in session and session["is_admin"]:
        shows = Query("shows", check_attrs={"venue_id": id}).call_select_query()
        results = [dict(row) for row in shows]
        return results
    abort(401)


@app.route("/venues", methods=["POST"])
def create_venue():
    if "is_admin" in session and session["is_admin"]:
        while True:
            error = False
            try:
                name = request.form["name"]
                multiplier = int(request.form["multiplier"])
                capacity = int(request.form["capacity"])
                place = request.form["place"]
                location = request.form["location"]
            except ValueError:
                error = "Invalid Values: Value not a number"
                break
            except Exception as e:
                error = "Invalid Form Values: " + str(e)
                break
            venue = Query("venues", check_attrs={"name": name}).call_select_query(
                one=True
            )
            if venue:
                error = "Venue already exists"
                break
            status = Query(
                "venues",
                other_attrs={
                    "name": name,
                    "multiplier": multiplier,
                    "capacity": capacity,
                    "place": place,
                    "location": location,
                },
            ).call_insert_query()
            if status == "Success":
                return render_template("success.html")
            else:
                return render_template("failure.html", error=status)

    abort(401)


@app.route("/venues/<int:id>", methods=["PUT"])
def edit_venue(id):
    if "is_admin" in session and session["is_admin"]:
        while True:
            error = False
            try:
                name = request.form["name"]
                multiplier = int(request.form["multiplier"])
                capacity = int(request.form["capacity"])
                place = request.form["place"]
                location = request.form["location"]
            except ValueError:
                error = "Invalid Values: Value not a number"
                break
            except Exception as e:
                error = "Invalid Form Values: " + str(e)
                break
            venue = Query("venues", check_attrs={"id": id}).call_select_query(one=True)
            if not venue:
                abort(400)
            status = Query(
                "venues",
                other_attrs={
                    "name": name,
                    "multiplier": multiplier,
                    "capacity": capacity,
                    "place": place,
                    "location": location,
                },
                check_attrs={"id": id},
            ).call_update_query()
            if status == "Success":
                return render_template("success.html")
            else:
                return render_template("failure.html", error=status)
    abort(401)


@app.route("/venues/<int:id>", methods=["DELETE"])
def delete_venue(id):
    if "is_admin" in session and session["is_admin"]:
        status = Query("venues", check_attrs={"id": id}).call_delete_query()
        return status
    abort(401)
