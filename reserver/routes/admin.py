from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.routes.venue import get_venues, delete_venue, get_venue_shows


@app.route("/admin/home", methods=["GET", "POST"])
def admin_home():
    if request.method == "POST":
        pass
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
    status = delete_venue(id)
    if status == "Success":
        return redirect(request.referrer)
    else:
        return render_template("failure.html", error=status)
