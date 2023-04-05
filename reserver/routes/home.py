from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.routes.venue import get_venues


@app.route("/", methods=["GET"])
def home():
    if "userid" in session:
        if session["is_admin"]:
            return redirect(url_for("admin_home"))
        else:
            return redirect(url_for("user_home"))
    return render_template("landing.html")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/user/home", methods=["GET", "POST"])
def user_home():
    if request.method == "POST":
        pass
    if "userid" in session and "is_admin" in session:
        if session["is_admin"]:
            return redirect(url_for("admin_home"))
        else:
            return render_template("user_home.html")
    else:
        return redirect(url_for("login"), error="Please Log-in to continue")


@app.route("/admin/home", methods=["GET", "POST"])
def admin_home():
    if request.method == "POST":
        pass
    if "userid" in session and "is_admin" in session:
        if not session["is_admin"]:
            return redirect(url_for("user_home"))
        else:
            venues = get_venues()
            return render_template(
                "admin_home.html", name=session["username"], venue_list=venues
            )
    else:
        return redirect(url_for("login"), error="Please Log-in to continue")
