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

    name = request.args.get('name')
    address = request.args.get('address')
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    session["address"] = address
    session["lat"] = lat
    session["lng"] = lng
    print session

    raw_data = api_data_handler.meetup_api_call(lat, lng, api_key)
    # print pprint(raw_data)
    clean_data = api_data_handler.meetup_jsonify_events(raw_data)
    # print pprint(clean_data)

    return jsonify(clean_data)


@app.route('/registration')
def render_registration_page():
    """Shows registration page"""

    return render_template("registration.html")


@app.route('/handle-regis', methods=['GET', 'POST'])
def save_user_in_database():
    """Register new user and save info in database"""

    name = request.form.get("name")
    email = request.form.get("email") 
    regis_pw_input = request.form.get("password")

    # Check if user is already registered
    if User.query.filter_by(email=email).first() is not None:
        flash("There is already an account registered with this email.")
        return redirect("/registration")

    # Hash password to save in database
    hashed_pw = bcrypt.hash(regis_pw_input)
    del regis_pw_input    

    # Add address record in DB 
    if session != None:
        address = Address(lat=session["lat"], lng=session["lng"], formatted_addy=session["address"])
        db.session.add(address)
        db.session.flush()

    # Add user record in DB 
    if address.addy_id:
        user = User(name=name, email=email, password=hashed_pw, addy_id=address.addy_id)
    else:
        user = User(name=name, email=email, password=hashed_pw)

    db.session.add(user)
    db.session.commit() 


    flash("registration was successful")

    return redirect("/") 


@app.route('/login')
def render_login_page():
    """Shows the registration and login page. Gives user access to profile."""

    return render_template("login.html")

    #import user manager.login 


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


# @app.route('/logout')
# def logout_user():
#     """Logs user out of session"""

#     if session: #save data in session
#         del session['user_id']
#         flash("Logout successful!")
#     else:
#         flash("You have to log in first.")

#     return redirect("/")

@app.route('/favorite')
def save_event_in_database():
    """Saves event information in database when user favorites""" 

    name = request.args.get('name')
    url = request.args.get('url')
    return "My event: ", name
#     name = request.args.get('name')
#     time = request.args.get('time')
#     url = request.args.get('url')
#     position = request.args.get('position')
#     user_id = #some SQLAlchemy query 
#     addy_id = 
#     catevt_id =

#     event = Saved_event()
#     datetime = db.Column(db.DateTime, nullable=False)
#     name = db.Column(db.String(150), nullable=False)
#     url = db.Column(db.String(500), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     addy_id = db.Column(db.Integer, db.ForeignKey('addresses.addy_id'), nullable=False)


# @app.route('/meetup-event-search')
# def search_specific_meetup_event():
#     """Request events from Meetup API and returns a JSON with local events."""

#     evt_id = request.args.get('evt_id')


#     session["address"] = address
#     session["lat"] = lat
#     session["lng"] = lng
#     print session

#     raw_data = api_data_handler.meetup_api_call(lat, lng, api_key)
#     # print pprint(raw_data)
#     clean_data = api_data_handler.meetup_jsonify_events(raw_data)
#     # print pprint(clean_data)

#     return jsonify(clean_data)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')