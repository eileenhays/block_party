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

    return render_template("homepage.html")


@app.route('/search-events')
def search_for_events():
    """Request events from Meetup API given location."""

    set_radius = 1 #default distance in mile(s) from location
    # lat = request.args.get('latitude')
    # lng = request.args.get('longitude')
    lat = 37.7893921
    lng = -122.4099426

    payload = {'key': api_key, 'sign': 'true', 'photo-host': 'public',
               'lat': lat, 'lon': lng, 'radius': set_radius,
               'page': 3}
    url = 'https://api.meetup.com/2/open_events'
    response = requests.get(url, params=payload)
    data = response.json()
    event_list = search_events(data)

    return render_template("map.html", event_list=event_list)

@app.route('/render-test')
def render_test_template():
    """Renders the test.html file for testing purposes."""

    return render_template('test.html')


#******************* HELPER METHODS ****************************
def search_events(data):
    """"Parses out relevant data from the Meetup API response.
    Name, description, url, lat, long, and rsvp_num."""

    events_list = data['results']

    map_events = []

    for event in events_list:
        event_dict = {}
        event_dict['name'] = event['name']
        event_dict['description'] = event['description']
        event_dict['time'] = event['time']
        event_dict['utc_offset'] = event['utc_offset']    
        event_dict['url'] = event['event_url']
        if 'venue' in event:
            event_dict['lat'] = event['venue']['lat']
            event_dict['lng'] = event['venue']['lon']
        else: #check if group is the actual default location
            event_dict['lat'] = event['group']['group_lat']
            event_dict['lng'] = event['group']['group_lon']
        event_dict['rsvp_num'] = event['yes_rsvp_count']

        map_events.append(event_dict)

    return map_events


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
