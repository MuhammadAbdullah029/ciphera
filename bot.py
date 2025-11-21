from flask import Flask, render_template, request, redirect, url_for, session
import aiml
import glob
import hashlib
import os

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY_HERE"


k = aiml.Kernel()
for aiml_file in glob.glob('data/*.aiml'):
    k.learn(aiml_file)

USERS_FILE = "users.txt"


# ---------- USER DATA FUNCTIONS ----------
def save_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")


def validate_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False

    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pwd = line.strip().split(",")
            if username == user and pwd == hashed:
                return True
    return False



@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", username=session["username"])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        save_user(username, password)
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid username or password"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/get")
def get_bot_response():
    if "username" not in session:
        return "Please log in to chat."

    query = request.args.get("msg")
    response = k.respond(query)
    return response if response else ":)"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
