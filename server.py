"""Community Events Server File"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db #<import classes>
#libraries for API requests
from sys import argv
from pprint import pprint, pformat
import os
import requests
import json
import data_clean


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
    """Request events from Meetup API location input from user, and
    returns a JSON with local events."""

    # Search coordinates
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    #Use for testing purposes
    # lat = 37.7893921
    # lng = -122.40775389999999

    # Search parameters
    search_radius = 2 #default distance in mile(s) from location
    search_time = ',2w' #upcoming for the week
    num_of_results = 3

    payload = {'key': api_key, 
               'time': search_time, 
               'sign': 'true', 
               'photo-host': 'public',
               'lat': lat, 
               'lon': lng, 
               'radius': search_radius,
               'page': num_of_results}
    url = 'https://api.meetup.com/2/open_events'

    response = requests.get(url, params=payload)
    data = response.json()
    clean_data = data_clean.meetup_jsonify_events(data)

    return jsonify(clean_data)


# def open_json_data(filename):
#     data = json.loads(open(filename))
#     return data

# @app.route('/test')
# def render_test():
#     """This is to test my functions"""

#     filename = open('./seed_data/messy_test.json')
#     data = json.loads(filename)
#     return render_template("test.html", data=str(data))

# @app.route('/saved-address')
# def save_address_in_database(event_record):
#     """Saves address information in database tied to user."""

#     pass 
#     lat = request.args.get('lat')
#     lng = 
#     formatted_addy = 

# @app.route('/saved-user', method=["POST"])
# def save_user_in_database(event_record):
#     """Saves user information in database tied to user."""

#     pass 
    

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

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')