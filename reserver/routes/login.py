from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.db_methods import query_db


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
        print(request.form)
        username = request.form["username"]
        password = request.form["password"]
        user = query_db(
            "SELECT * FROM users WHERE username = ?",
            [username],
            one=True,
        )
        if user:
            print(user)
            if user["password"] == password:
                session["username"] = user["username"]
                session["is_admin"] = False
                return redirect(url_for("home"))
            else:
                error = "Password Mismatch"
        else:
            error = "Username not found!"
    return render_template("login.html", error=error)
