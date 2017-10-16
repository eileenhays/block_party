"""Community Events Server File"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session, abort, url_for)
from flask_debugtoolbar import DebugToolbarExtension

#libraries for API requests
from sys import argv
from pprint import pprint, pformat

from model import db, connect_to_db, User, Address
import os
import api_data_handler
from passlib.hash import bcrypt

from flask_login import LoginManager, login_user, login_required, logout_user 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
api_key = os.environ.get('MEETUP_API_KEY')

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
    flash("registration was successful<br> user logged in")

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
    logout_user()
    print session
    flash("Logout successful!")
    return redirect('/')

@app.route('/add-fave')
@login_required
def save_event_in_database():
    """Saves event information in database when user favorites""" 

    pass
    name = request.args.get('name')
    url = request.args.get('url')
    return "My event: ", name


@app.route('/favorites')
@login_required
def render_favorites_page():
    """Shows user's favorites""" 

    return render_template("favorites.html")


@app.route('/profile')
@login_required
def render_profile_page():

    return render_template("profile.html")


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