import sqlite3

from flask import Flask, redirect, render_template, request


app = Flask(__name__)

rdb = sqlite3.connect('myDatabase.db', check_same_thread=False)

SPORTS = ["Dodgeball", "Flag Football", "Soccer", "Volleyball", "Ultimate Frisbee"]


@app.route('/')

def index():

    return render_template("index.html", sports=SPORTS)


@app.route('/register', methods=["POST"])

def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or not sport:
        return render_template("failure.html", message="Needs Name" if not name else "Needs Select a valid Sport")
    if sport not in SPORTS:
         return render_template("failure.html", message="Needs Select a valid Sport")
    
    rdb.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", (name, sport))

    return redirect("/registrants")

@app.route("/registrants")

def registrants():
    registrants = rdb.execute("SELECT * FROM registrants")
    return render_template("success.html", registrants=registrants)