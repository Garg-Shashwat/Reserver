from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.db_methods import query_db, Query


@app.route("/register", methods=["GET", "POST"])
def register():
    error = False
    if request.method == "POST":
        while True:
            try:
                email = request.form["email"]
                username = request.form["username"]
                age = int(request.form["age"])
                password = request.form["password"]
                conf_pass = request.form["confirm-password"]
                firstname = request.form["firstname"]
                lastname = request.form["lastname"]
                gender = request.form["gender"]
            except ValueError:
                error = "Invalid Age: Value not a number"
                break
            except Exception as e:
                error = "Invalid Form Values: " + str(e)
                break

            db_email = Query("users", {"email": email}, ["email"]).call_select_query(
                one=True
            )
            if db_email:
                error = "Email Already Registered"
                break

            user = Query(
                "users", {"username": username}, ["username"]
            ).call_select_query(one=True)
            if user:
                error = "Username Already Taken"
                break

            if age < 12 or age > 117:
                error = "Invalid Age: Enter a valid number (12-117)"
                break
            if password != conf_pass:
                error = "Password and confirm password did not match"
                break

            status = Query(
                "users",
                {
                    "email": email,
                    "username": username,
                    "age": age,
                    "password": password,
                    "first_name": firstname,
                    "last_name": lastname,
                    "gender": gender,
                },
            ).call_insert_query()
            if status == "Success":
                return render_template("success.html")
            else:
                return render_template("register.html", error=status)

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Query(
            "users", {"username": username}, ["username", "password"]
        ).call_select_query(one=True)
        if user:
            if user["password"] == password:
                session["username"] = user["username"]
                session["is_admin"] = False
                return redirect(url_for("home"))
            else:
                error = "Password Mismatch"
        else:
            error = "Username not found!"
    return render_template("login.html", error=error)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Query(
            "admins", {"username": username}, ["username", "password"]
        ).call_select_query(one=True)
        if user:
            if user["password"] == password:
                session["username"] = user["username"]
                session["is_admin"] = True
                return redirect(url_for("home"))
            else:
                error = "Password Mismatch"
        else:
            error = "Username not found!"
    return render_template("login.html", error=error, mode="admin")
