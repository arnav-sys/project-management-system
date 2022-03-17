from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "D"
db = SQLAlchemy(app)

logged_in = False
current_user = None

def required(func):
    def wrapper():
        global logged_in
        if logged_in == True:
            print("he is logged in")
            return func()
        else:
            print("not working")
            return redirect("http://localhost:3000/login")

    return wrapper

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250),nullable=False)

db.create_all()

@app.route("/", methods=["get"])
def home():
    global logged_in
    global current_user
    if logged_in == True:
        return render_template("index.html",is_logged_in=logged_in,user=current_user)
    return render_template("index.html",is_logged_in=logged_in)

@app.route("/login", methods=["GET","POST"])
def login():
    message = ""
    global logged_in
    if logged_in == False:
        if request.method == "POST":
            email = request.form.get("Email")
            password = request.form.get("Password")
            if db.session.query(User).filter_by(email=email).count() == 1:

                correct_user =User.query.filter_by(email=email)[0]

                if correct_user.password == password:
                    logged_in = True
                    global current_user
                    current_user = correct_user
                    logged_in = True
                    return redirect("http://localhost:3000/dashboard")
                else:
                    message = "wrong password"
            
            else:
                message = "No user found"
    else:
        return redirect("http://localhost:3000/dashboard")
    return render_template("login.html", message = message)
          

@app.route("/signup", methods=["POST","GET"])
def signup():
    message = ""
    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("Email")
        password = request.form.get("Password")
        if db.session.query(User).filter_by(email=email).count() < 1:
            new_user = User(name=name, email=email, password=password)
            global current_user
            current_user = new_user
            db.session.add(new_user)
            db.session.commit()
            global logged_in
            logged_in = True
            return redirect("http://localhost:3000/dashboard")
        else:
            message="user already exists"
    return render_template("signup.html", message=message)

@app.route("/logout")
def logout():
    global current_user
    global logged_in
    current_user = None
    logged_in = False
    return redirect("http://localhost:3000/login")

@app.route("/dashboard")
@required
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(port=3000, debug=True)