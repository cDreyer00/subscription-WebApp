import sqlite3, os
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_DEFAULT_SENDER")
mail = Mail(app)

rdb = sqlite3.connect('myDatabase.db', check_same_thread=False)

TEAMS = ["A", "B", "C", "D"]

@app.route('/')

def index():
    print(os.getenv("MAIL_DEFAULT_SENDER"))
    print(os.getenv("MAIL_PASSWORD"))
    return render_template("index.html", teams=TEAMS)


@app.route('/register', methods=["POST"])

def register():
    email = request.form.get("email")
    team = request.form.get("team")

    if not email or not team:
        return render_template("failure.html", message="Missing email" if not email else "Needs Select a valid Sport")
    if team not in TEAMS:
         return render_template("failure.html", message="Needs Select a valid Sport")
    
    rdb.execute("INSERT INTO registrants (email, team) VALUES(?, ?)", (email, team))
    rdb.commit()

    message = Message("You are registered in team: " + team, recipients=[email])
    mail.send(message)
    return redirect("/registrants")

@app.route("/registrants")

def registrants():
    registrants = rdb.execute("SELECT * FROM registrants")    
    return render_template("success.html", registrants=registrants)