from flask import Flask
import hashlib
from flask import render_template, request
from models.user import User
from models.settings import db

app = Flask(__name__)


# db.create_all()

@app.route('/', methods=["GET"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def index():
    return render_template("layout.html")


@app.route('/login', methods=["GET", "POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        tryUser = db.query(User).filter_by(email=email).first()

        if not tryUser:
            return "This user does not exist - try registration on /register"
        else:
            tryPassword = hashlib.sha256(password.encode()).hexdigest()
            if tryPassword == tryUser.password:
                return "Welcome, %s" % tryUser.email
            else:
                return "Wrong username/password!"


@app.route('/register', methods=["GET", "POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        newUser = User(email=email, password=hashlib.sha256(password.encode()).hexdigest())
        db.add(newUser)
        db.commit()
        return "Sučes"


if __name__ == '__main__':
    app.run(use_reloader=True)
