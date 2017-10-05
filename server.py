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

    set_radius = 2 #default distance in mile(s) from location
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    #Use for testing purposes
    # lat = 37.7893921
    # lng = -122.40775389999999


    payload = {'key': api_key, 'sign': 'true', 'photo-host': 'public',
               'lat': lat, 'lon': lng, 'radius': set_radius,
               'page': 3}
    url = 'https://api.meetup.com/2/open_events'
    response = requests.get(url, params=payload)
    data = response.json()
    clean_data = data_clean.meetup_jsonify_events(data)

    return jsonify(clean_data)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')