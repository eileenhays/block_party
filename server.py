"""Community Score Server File"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db #<import classes>
import os

google_api_key = os.environ['GOOGLE_MAPS_API_KEY']
walkscore_api_key = os.environ['WALKSCORE_API_KEY']


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html", google_api_key=google_api_key)


@app.route("/users/<user_id>")
def load_user_profile(user_id):
    """Returning details for specific user:
        Name
        Email
        Link to addresses saved
    """
    pass

    user = User.query.filter_by(user_id=user_id).one()

    return render_template("", user=user)


@app.route("/calculate_score")
def calculate_score():
    """Calculates community score"""
    pass


@app.route("/registration")
def show_registration():
    """Shows registration form."""
    pass
    return render_template(".html")


@app.route("/user-data", methods=["POST"])
def new_user():
    """Register new user and input into database."""
    pass
    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first() is not None:
        return "There was already an account registered by this email."

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/log-in")
def show_login():
    """Shows Log-in form."""
    pass
    return render_template(".html")


@app.route("/handle-log-in", methods=["POST"])
def handles_login():
    """Checks email against password in database and fetches user_id for Flask
    session.
    """
    pass
    curr_email = request.form.get("email")
    curr_password = request.form.get("password")

    db_user = User.query.filter_by(email=curr_email).first()
    db_password = db_user.password
    db_user_id = db_user.user_id

    if db_user is not None and curr_password == db_password:
        session['user_id'] = db_user_id
        flash("Successfully logged in!")
        print session
        return redirect("/users/" + str(db_user_id))
    else:
        flash("Wrong password!")
        return redirect("/log-in")


@app.route("/log-out")
def handles_logout():
    """Logs user out."""
    pass


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
