"""BLOCK PARTY Server File"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session, abort, url_for)
from flask_cache import Cache
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
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.secret_key = "ABC"
connect_to_db(app)

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


@app.route('/landing')
def render_landing():
    """Landing page"""

    return render_template("landing.html")


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

    # Meetup query
    mtup_data = Meetup_API.find_events(lat, lng)
    clean_data = Meetup_API.sanitize_data(mtup_data)
    # Eventbrite query
    eb_data = Eventbrite_API.find_events(lat, lng)
    clean_eb_data = Eventbrite_API.sanitize_data(eb_data)
    clean_data.update(clean_eb_data)

    return jsonify(clean_data)


@app.route('/about')
def render_about_page():
    """Shows about page""" 

    return render_template("about.html")


@app.route('/registration', methods=['GET'])
def render_registration_page():
    """Shows registration page"""

    return render_template("registration.html")


@app.route('/registration', methods=['POST'])
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
    if 'lat' and 'lng' in session:
        new_address = Address(lat=session["lat"], lng=session["lng"], formatted_addy=session["address"])
        db.session.add(new_address)
        db.session.flush()
        # Add user record in DB 
        new_user = User(name=name, email=email, password=hashed_pw, addy_id=new_address.addy_id)
    else:
        new_user = User(name=name, email=email, password=hashed_pw, addy_id=None)

    db.session.add(new_user)
    db.session.commit() 

    login_user(new_user)

    print "registration was successful and user logged in"
    flash("registration was successful and user logged in")

    return redirect("/") 


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)


@app.route('/login', methods=['GET'])
def render_login_page():
    """Shows the registration and login page. Gives user access to profile."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def check_login():
    """Verify login credentials"""

    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    password = user.password

    if bcrypt.verify(request.form.get("password"), password):
        # Login and validate the user.
        login_user(user)

        flash('Login was successful')

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
 
    logout_user()
    session.clear()
    print 'session', session

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
                              src_id=src_id
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

    return render_template("favorites.html", 
                           saved_events=saved_events, 
                           past_events=past_events, 
                           error="You currently have no favorites")


@app.route('/remove-event', methods=["POST"])
@login_required
def remove_event_from_faves():
    """Deletes user_evt entry from database when user clicks remove"""

    user_id = current_user.user_id 
    evt_id = request.form.get("evt_id") 

    user_evt = User_saved_event.query.filter(and_(User_saved_event.user_id == user_id,
                                                  User_saved_event.evt_id == evt_id)).first()

    db.session.delete(user_evt)
    db.session.commit()

    print "Event was removed from %s's favorites" % (current_user.name)

    remove_evt = Saved_event.query.filter(Saved_event.evt_id==evt_id).first() 

    return remove_evt.name


@app.route('/update-homebase', methods=["POST"])
@login_required
def update_homebase_address():
    """Updates the home address for the user to current session"""

    address = session["address"] 
    lat = session["lat"]
    lng = session["lng"]

    new_address = Address(lat=lat, lng=lng, formatted_addy=address)
    db.session.add(new_address)
    db.session.flush()

    #change address for the user
    curr_user = User.query.filter_by(user_id=current_user.user_id).first()
    curr_user.addy_id = new_address.addy_id
    db.session.commit()

    return new_address.formatted_addy


@app.route('/homebase-in-session')
def autoload_homebase():
    """Returns homebase address to autopopulate"""

    if 'user_id' in session:
        curr_user = User.query.filter_by(user_id=current_user.user_id).first()
        homebase_obj = Address.query.filter_by(addy_id=curr_user.addy_id).first()

        if homebase_obj is not None:
            return homebase_obj.formatted_addy
    return 'None'


# @app.route('/date-sort', methods=["POST"])
# @login_required
# def sort_events_by_date():
#     """Sorts the favorite events by date from earliest to latest"""

#     user_id = current_user.user_id
#     user_saved_events = User_saved_event.query.filter_by(user_id=user_id).all()
    
#     saved_events = []
#     past_events = []

#     for user_evt in user_saved_events:
#         evt_id = user_evt.event.evt_id
#         saved_event = Saved_event.query.filter(Saved_event.evt_id==evt_id).first()
        
#         if saved_event.datetime >=datetime.today():
#             saved_events.append(saved_event)
#         else: 
#             past_events.append(saved_event)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')