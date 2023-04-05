from flask import jsonify, request, session, redirect, render_template, url_for, abort

from reserver import app
from reserver.db_methods import query_db, Query
from reserver.error_handler import handle_exception


@app.route("/shows", methods=["GET"])
def get_shows():
    if "is_admin" in session and session["is_admin"]:
        shows = Query("shows").call_select_query()
        results = [tuple(row) for row in shows]
        return results
    abort(401)


@app.route("/shows/<int:id>", methods=["GET"])
def get_show(id):
    if "is_admin" in session and session["is_admin"]:
        show = Query("shows", check_attrs={"id": id}).call_select_query(one=True)
        return jsonify(tuple(show))
    abort(401)


@app.route("/shows", methods=["POST"])
def create_show():
    if "is_admin" in session and session["is_admin"]:
        while True:
            error = False
            try:
                name = request.form["name"]
                rating = int(request.form["rating"])
                tags = request.form["tags"]
                price = int(request.form["price"])
                timing = request.form["timing"]
            except ValueError:
                error = "Invalid Values: Value not a number"
                break
            except Exception as e:
                error = "Invalid Form Values: " + str(e)
                break
            status = Query(
                "shows",
                other_attrs={
                    "name": name,
                    "rating": rating,
                    "tags": tags,
                    "price": price,
                    "timing": timing,
                },
            ).call_insert_query()
            if status == "Success":
                return render_template("success.html")
            else:
                return render_template("failure.html", error=status)

    abort(401)


@app.route("/shows/<int:id>", methods=["PUT"])
def edit_show(id):
    if "is_admin" in session and session["is_admin"]:
        while True:
            error = False
            try:
                name = request.form["name"]
                rating = int(request.form["rating"])
                tags = request.form["tags"]
                price = int(request.form["price"])
                timing = request.form["timing"]
            except ValueError:
                error = "Invalid Values: Value not a number"
                break
            except Exception as e:
                error = "Invalid Form Values: " + str(e)
                break
            show = Query("shows", check_attrs={"id": id}).call_select_query(one=True)
            if not show:
                abort(400)
            status = Query(
                "shows",
                other_attrs={
                    "name": name,
                    "rating": rating,
                    "tags": tags,
                    "price": price,
                    "timing": timing,
                },
                check_attrs={"id": id},
            ).call_update_query()
            if status == "Success":
                return render_template("success.html")
            else:
                return render_template("failure.html", error=status)
    abort(401)


@app.route("/shows/<int:id>", methods=["DELETE"])
def delete_show(id):
    if "is_admin" in session and session["is_admin"]:
        status = Query("shows", check_attrs={"id": id}).call_delete_query(one=True)
        if status == "Success":
            return render_template("success.html")
        else:
            return render_template("failure.html", error=status)
    abort(401)
