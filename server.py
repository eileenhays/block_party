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
import api_data_handler


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

    # print "Raw data:"
    # print raw_data 
    # print "\n\n\n"
    # print "Clean data:"
    # print clean_data 
    # print "\n\n\n"

    return jsonify(clean_data)



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