from flask import Flask
import hashlib
from flask import render_template, request, make_response, redirect, url_for
from models.user import User
from models.settings import db
import uuid;

app = Flask(__name__)


# db.create_all()

@app.route('/', methods=["GET"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def index():
    return render_template("index.html")


@app.route('/login', methods=["POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    tryUser = db.query(User).filter_by(email=email).first()

    if not tryUser:
        return "This user does not exist - try registration on /register"
    else:
        tryPassword = hashlib.sha256(password.encode()).hexdigest()
        # print(tryUser)
        # exit()
        if tryPassword == tryUser.password:
            # tryUser.session_token = uuid.uuid4()
            # db.commit(tryUser) { session_token : "token" }
            # db.query(User).filter_by(email=email).update(dict(session_token=uuid.uuid4().__str__()))
            # db.commit()

            tryUser.session_token = uuid.uuid4().__str__()
            db.add(tryUser)
            db.commit()

            response = make_response(redirect(url_for("dashboard")))
            # print(response)
            # exit()
            response.set_cookie("session_token", tryUser.session_token, httponly=True, samesite='Strict')

            return response
        else:
            return "Wrong username/password!"


@app.route('/register', methods=["GET", "POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- Controller
def register():
    if request.method == "GET":
        url = request.url_rule
        return render_template("register.html", url=url)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        newUser = User(email=email, password=hashlib.sha256(password.encode()).hexdigest())
        db.add(newUser)
        db.commit()
        return "Sučes"


@app.route('/dashboard', methods=["GET"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- Controller
def dashboard():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None

    if user:
        return render_template("dashboard.html", user=user)
    else:
        response = make_response(redirect(url_for("index")))
        return response

    return "welcome to dashboard"


if __name__ == '__main__':
    app.run(use_reloader=True, port=12345)
