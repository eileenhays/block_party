"""Community Events Server File"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension

#libraries for API requests
from sys import argv
from pprint import pprint, pformat

from model import db, connect_to_db, User, Address
import os
import api_data_handler
from passlib.hash import bcrypt


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
api_key = os.environ.get('MEETUP_API_KEY')

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage with map."""

    return render_template("map.html")


@app.route('/search-events')
def search_for_events():
    """Request events from Meetup API and returns a JSON with local events."""

    lat = request.args.get('lat')
    lng = request.args.get('lng')

    raw_data = api_data_handler.meetup_api_call(lat, lng, api_key)
    clean_data = api_data_handler.meetup_jsonify_events(raw_data)

    print pprint(raw_data)

    return jsonify(clean_data)


@app.route('/save-user', methods=['GET', 'POST'])
def save_user_in_database():
    """Register new user and save info in database"""

    name = request.form.get("name")
    email = request.form.get("email") 
    regis_pw_input = request.form.get("password")

    if User.query.filter_by(email=email).first() is not None:
        flash("There is already an account registered with this email.")
        return redirect("/save-user")

    hashed_pw = bcrypt.hash(regis_pw_input)
    del regis_pw_input    

    user = User(name=name, email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit() 

    flash("registration was successful")

    return redirect("/") 


@app.route('/login')
def render_login_page():
    """Shows the registration and login page"""

    return render_template("regis-login.html")


@app.route('/handle-login', methods=['POST'])
def check_login():
    """Verify login credentials"""

    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    password = user.password

    if bcrypt.verify(request.form.get("password"), password):
        flash("Login successful!")
        return redirect("/")
    else:
        flash("Email and/or password are invalid. Try again.")
        return redirect("/login")


# @app.route('/saved-address')
# def save_address_in_database(event_record):
#     """Saves address information in database tied to user."""

#     pass 
#     lat = request.args.get('lat')
#     lng = 
#     formatted_addy =     

# @app.route('/saved-event')
# def save_event_in_database(event_record):
#     """Saves event information in database tied to user."""

#     pass 

#     datetime = request.args.get('datetime')
#     name = request.args.get('name')
#     url = request.args.get('url')
#     user_id = #some SQLAlchemy query 
#     addy_id = 
#     catevt_id =

# # HELPER FUNCTIONS

# def hashed_password(regis_pw_input):
#     """Hashes a user input password"""

#     # generate new salt, hash password
#     hashed = bcrypt.hash(regis_pw_input)

#     del regis_pw_input
#     return hashed


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')