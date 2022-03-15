from distutils.log import debug
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["get"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["get"])
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(port=3000, debug=True)