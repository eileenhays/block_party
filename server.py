"""BLOCK PARTY Server File"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session, abort, url_for)
from flask_debugtoolbar import DebugToolbarExtension

#libraries for API requests
from sys import argv
from pprint import pprint, pformat

from model import db, connect_to_db, User, Address, Saved_event, Category, User_saved_event, Source
from meetup_handler import Meetup_API
from eventbrite_handler import Eventbrite_API
from passlib.hash import bcrypt

from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
import os
from datetime import datetime
from sqlalchemy import and_


app = Flask(__name__)
app.secret_key = "ABC"


# Raises an error in Jinja
app.jinja_env.undefined = StrictUndefined

######################################
#For Registration and Login
######################################

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'render_login_page'


@app.route('/')
def index():
    """Homepage with map."""

    return render_template("map.html")


@app.route('/search-events')
def search_for_events():
    """Request events from Meetup API and returns a JSON with local events."""

    address = request.args.get('address')
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    session["address"] = address
    session["lat"] = lat
    session["lng"] = lng
    print session

    raw_data = Meetup_API.find_events(lat, lng)
    clean_data = Meetup_API.sanitize_data(raw_data)

    # results = Eventbrite_API.find_events(lat, lng)
    # limit_results = {}

    # while len(limit_results) <= 10:
    #     for k, v in results:
    #         limit_results[k] = v

    # clean_data = Eventbrite_API.sanitize_data(limit_results)
    # print clean_data
    return jsonify(clean_data)


@app.route('/registration')
def render_registration_page():
    """Shows registration page"""

    return render_template("registration.html")


@app.route('/handle-regis', methods=['POST'])
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
        new_address = Address(lat=session["lat"], lng=session["lng"], formatted_addy=session["address"])
        db.session.add(new_address)
        db.session.flush()

    # Add user record in DB 
    if new_address.addy_id:
        new_user = User(name=name, email=email, password=hashed_pw, addy_id=new_address.addy_id)
    else:
        new_user = User(name=name, email=email, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit() 

    login_user(new_user)

    print "registration was successful and user logged in"
    flash("registration was successful and user logged in")

    return redirect("/") 


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)


@app.route('/login')
def render_login_page():
    """Shows the registration and login page. Gives user access to profile."""

    return render_template("login.html")


@app.route('/handle-login', methods=['POST'])
def check_login():
    """Verify login credentials"""

    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    password = user.password

    if bcrypt.verify(request.form.get("password"), password):
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return abort(400)

        return redirect(next or url_for('index'))

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    """Logs user out of their session"""
 
    # session.clear()
    logout_user()
    print session
    flash("Logout successful!")
    return redirect('/')


@app.route('/add-fave', methods=['POST'])
@login_required
def save_event_in_database():
    """Saves event information in database when user favorites""" 
    
    src_evt_id = request.form.get("src_evt_id")
    # Check if there is an event entry in database already
    if Saved_event.query.filter_by(src_evt_id='src_evt_id').first() is None:
        # get all info from event    
        datetime = request.form.get("datetime")
        name = request.form.get("name")
        url = request.form.get("url")
        group_name = request.form.get("group_name")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        address = request.form.get("address")
        category = request.form.get("cat")
        cat_id = Category.query.filter_by(name=category).first()
        src_id = request.form.get("src_id")

        # add event address 
        new_address = Address(lat=lat, lng=lng, formatted_addy=address)
        db.session.add(new_address)
        db.session.flush()

        #add event info 
        new_evt = Saved_event(src_evt_id=src_evt_id, 
                              datetime=datetime, 
                              name=name, 
                              url=url, 
                              group_name=group_name, 
                              addy_id=new_address.addy_id, 
                              cat_id=cat_id,
                              src_id=src_id,
                              )

        db.session.add(new_evt)
        db.session.flush()
        evt_id = new_evt.evt_id
    else:
        event = Saved_event.query.filter_by(src_evt_id=src_evt_id).first()
        evt_id = event.event.evt_id 
 
    new_user_saved_event = User_saved_event(user_id=current_user.user_id, evt_id=evt_id)
    db.session.add(new_user_saved_event)

    db.session.commit() 

    print "New event was added to favorites"
    return name


@app.route('/favorites')
@login_required
def render_favorites_page():
    """Shows user's favorites""" 

    user_id = current_user.user_id
    user_saved_events = User_saved_event.query.filter_by(user_id=user_id).all()
    
    saved_events = []
    past_events = []

    for user_evt in user_saved_events:
        evt_id = user_evt.event.evt_id
        saved_event = Saved_event.query.filter(Saved_event.evt_id==evt_id).first()
        
        if saved_event.datetime >=datetime.today():
            saved_events.append(saved_event)
        else: 
            past_events.append(saved_event)

        # if saved_event != None:
        #     saved_events.append(saved_event)

        # print "Saved_evt", saved_event.name

    return render_template("favorites.html", 
                           saved_events=saved_events, 
                           past_events=past_events, 
                           error="You currently have no favorites")

# @app.route('/update-homebase')
# @login_required
# def update_homebase_address():
#     """Updates the address connected to the user."""

#     curr_user = User.query.filter_by(user_id=current_user.user_id).first()

#     address = session["address"] 
#     lat = session["lat"]
#     lng = session["lng"]

#     new_address = Address(lat=lat, lng=lng, formatted_addy=address)
#     db.session.add(new_address)

#     curr_user.addy_id = new_addy_id
#     db.commit()
#     db.session.flush()


# @app.route('/search-events-eb')
# def find_eb_events():
#     """Search for events in Eventbrite and returns sanitized data"""

#     lat = 37.7893921
#     lng = -122.40775389999999

#     results = Eventbrite_API.find_events(lat, lng)
#     clean_data = Eventbrite_API.sanitize_data(results)

#     return render_template("evt_analysis.html",
#                            # data=pformat(data),
#                            results=clean_data)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')