from flask import request, session, redirect, render_template, url_for, abort
import requests
import json

from reserver import app
from reserver.db_methods import Query


@app.route("/user/home", methods=["GET"])
def user_home():
    if "userid" in session and "is_admin" in session:
        if session["is_admin"]:
            return redirect(url_for("admin_home"))
        else:
            q = request.args.get("query")
            params = {}
            if q:
                params["query"] = q
            response = requests.get(
                request.host_url.rstrip("/") + url_for("get_venues"), params
            )
            venues = json.loads(response.text)

            return render_template(
                "user_home.html",
                name=session["username"],
                venue_list=venues,
            )
    else:
        return render_template("login.html", error="Please Log-in to continue")


@app.route("/user/show/book", methods=["GET", "POST"])
def book_show():
    if "userid" in session and "is_admin" in session:
        if session["is_admin"]:
            abort(400)
        if request.method == "GET":
            id = request.args.get("id")
            response = requests.get(
                request.host_url.strip("/") + url_for("get_show", id=id)
            )
            show = json.loads(response.text)
            info = dict(
                Query(
                    "venues",
                    check_attrs={"id": show["venue_id"]},
                    other_attrs=["capacity", "multiplier"],
                ).call_select_query(one=True)
            )
            seats = info["capacity"] - show["booked_seats"]
            price = info["multiplier"] * show["price"] / 100
            return render_template(
                "book_show.html",
                name=session["username"],
                show=show,
                seats=seats,
                price=price,
            )
        else:
            id = int(request.form.get("id"))
            booked_seats = int(request.form.get("book_seats"))
            userid = session["userid"]
            response = requests.get(
                request.host_url.strip("/") + url_for("get_show", id=id)
            )
            show = json.loads(response.text)
            info = dict(
                Query(
                    "venues",
                    check_attrs={"id": show["venue_id"]},
                    other_attrs=["capacity", "multiplier"],
                ).call_select_query(one=True)
            )
            price = (booked_seats * info["multiplier"] * show["price"]) / 100
            if booked_seats > info["capacity"] - show["booked_seats"]:
                abort(400)
            result = Query(
                "bookings",
                other_attrs={
                    "show_id": id,
                    "user_id": userid,
                    "show_name": show["name"],
                    "price": price,
                    "booked_seats": booked_seats,
                },
            ).call_insert_query()
            show_result = Query(
                "shows",
                check_attrs={"id": id},
                other_attrs={"booked_seats": show["booked_seats"] + booked_seats},
            ).call_update_query()
            print(result)
            print(show_result)
            if result == "Success":
                pass
            else:
                abort(500)
    else:
        return render_template("login.html", error="Please Log-in to continue")


@app.route("/user/bookings", methods=["GET", "POST"])
def show_bookings():
    if "userid" in session and "is_admin" in session:
        if request.method == "GET":
            if session["is_admin"]:
                abort(400)
            if request.method == "GET":
                userid = session["userid"]
                results = Query(
                    "bookings", check_attrs={"id": userid}
                ).call_select_query()
                bookings = [dict(row) for row in results]
                print(bookings)
            return render_template(
                "user_bookings.html",
                name=session["username"],
            )
    else:
        return render_template("login.html", error="Please Log-in to continue")
