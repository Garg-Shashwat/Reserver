from flask import request, session, redirect, render_template, url_for, abort

from reserver import app
from reserver.routes.venue import (
    get_venues,
    delete_venue,
    get_venue,
    edit_venue,
    create_venue,
    Venue,
)


@app.route("/admin/home", methods=["GET"])
def admin_home():
    if "userid" in session and "is_admin" in session:
        if not session["is_admin"]:
            return redirect(url_for("user_home"))
        else:
            venues = get_venues()
            # shows = get_venue_shows()
            return render_template(
                "admin_home.html",
                name=session["username"],
                venue_list=venues,
                # shows_list=shows,
            )
    else:
        return redirect(url_for("login"), error="Please Log-in to continue")


@app.route("/admin/venue/delete/<int:id>", methods=["GET"])
def admin_delete_venue(id):
    if "userid" in session and "is_admin" in session:
        status = delete_venue(id)
        if status == "Success":
            return redirect(request.referrer)
        else:
            return render_template("failure.html", error=status)
    else:
        return redirect(url_for("login"), error="Please Log-in to continue")


@app.route("/admin/venue/manage", methods=["GET", "POST"])
def admin_manage_venue():
    if "userid" in session and "is_admin" in session:
        if request.method == "GET":
            venue_id = request.args.get("v_id")
            if venue_id:
                venue = get_venue(venue_id)
                return render_template(
                    "manage_venue.html", name=session["username"], venue=venue
                )
            else:
                return render_template("manage_venue.html", name=session["username"])
        elif request.method == "POST":
            error = False
            while True:
                try:
                    type = request.form["type"]
                    if type == "Create":
                        name = request.form["name"]
                    else:
                        id = request.form["id"]
                    place = request.form["place"]
                    capacity = int(request.form["capacity"])
                    location = request.form["location"]
                except ValueError:
                    error = "Invalid Values"
                    break
                except Exception as e:
                    error = "Invalid Form Values: " + str(e)
                    break
                if type == "Create":
                    venue = Venue(capacity, place, location, name=name)
                    status = create_venue(venue)
                elif type == "Edit":
                    venue = Venue(capacity, place, location, id=id)
                    status = edit_venue(venue)
                else:
                    abort(400)
                if status != "Success":
                    error = status
                break
            if error:
                return render_template("failure.html", error=error)
            else:
                return redirect(url_for("admin_home"))
    else:
        return redirect(url_for("login"), error="Please Log-in to continue")
