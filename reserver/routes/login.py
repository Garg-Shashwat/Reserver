from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.db_methods import query_db, Query


@app.route("/register", methods=["GET", "POST"])
def register():
    error = False
    if request.method == "POST":
        while True:
            try:
                username = request.form["username"]
                age = int(request.form["age"])
                password = request.form["password"]
                conf_pass = request.form["confirm-password"]
                firstname = request.form["firstname"]
                lastname = request.form["lastname"]
                gender = request.form["gender"]
            except ValueError:
                error = "Invalid Age: Value not a number"
            except Exception as e:
                error = "Invalid Form Values: " + e
            user = query_db(
                "SELECT username FROM users WHERE username = ?",
                [username],
                one=True,
            )
            if user:
                error = "Username Already Taken"
                break
            if age < 12 or age > 117:
                error = "Invalid Age: Enter a valid number (12-117)"
                break
            if password != conf_pass:
                error = "Password and confirm password did not match"
                break

            print("Success")
            break

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
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
