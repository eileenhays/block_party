from datetime import datetime
import pytz
import requests
import json
import os
from pprint import pprint, pformat


class Eventbrite_API(object):

    EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_OAUTH_TOKEN')
    EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

    @classmethod
    def find_events(cls, lat, lng):
        """Uses specified parameters to make a call to the Meetup API"""

        distance = '2'
        measurement = 'mi'
        sort_by = 'date'

        distance = distance + measurement

        payload = {'location.latitude': lat,
                   'location.longitude': lng,
                   'location.within': distance,
                   'sort_by': sort_by,
                   }

        # For GET requests to Eventbrite's API, the token could also be sent as a
        # URL parameter with the key 'token'
        headers = {'Authorization': 'Bearer ' + cls.EVENTBRITE_TOKEN}

        response = requests.get(cls.EVENTBRITE_URL + "events/search/",
                            params=payload,
                            headers=headers)
        data = response.json()

        # If the response was successful (with a status code of less than 400),
        # use the list of events from the returned JSON
        if response.ok:
            events = data['events']
        # If there was an error (status code between 400 and 600), use an empty list
        else:
            flash(":( No parties: " + data['error_description'])
            events = []

        return events


    @classmethod
    def find_categories(cls):
        """API endpoint call that returns all Eventbrite categories"""

        headers = {'Authorization': 'Bearer ' + cls.EVENTBRITE_TOKEN}

        response = requests.get(cls.EVENTBRITE_URL + "/categories/",
                            headers=headers)
        categories_data = response.json()

        # write json data to file
        with open('eb_categories.json', 'w') as f:
          json.dump(categories_data, f)


    @classmethod
    def find_org(cls, org_id):
        """API endpoint call that returns organization name"""

        headers = {'Authorization': 'Bearer ' + cls.EVENTBRITE_TOKEN}

        response = requests.get(cls.EVENTBRITE_URL + "/categories/" + org_id + "/",
                            headers=headers)
        organization = response.json()

        return organization  


    @classmethod    
    def sanitize_data(cls, events_list):
        """"Parses out relevant data from the Meetup API response, and 
        dumps clean event info into JSON."""
        # print data

        map_events = {}
        #new dictionary created for every event
        for event in events_list:
            event_dict = {}

            if 'status' != 'canceled' or 'completed':
                event_dict['name'] = event['name']['text']
                if 'description' in event:
                    event_dict['description'] = event['description']
                event_dict['start_time'] = event['start']['local']  #sync up everywhere
                event_dict['end_time']  = event['end']['local']     
                event_dict['url'] = event['url']
                event_dict['group_name'] = event['organizer_id'] ## 
                event_dict['category'] = event['category_id'] ## 
                event_dict['format'] = event['format_id'] ##
                # event_dict['position'] = {}     
                event_dict['venue'] = event['venue_id']

                evt_id = event['id']
                map_events[evt_id] = event_dict #add each to map_events

        return map_events

# if __name__ == "__main__":
#   Eventbrite_API.find_categories()