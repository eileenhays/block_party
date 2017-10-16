from datetime import datetime
import pytz
import requests
import json

def convert_datetime_from_epoch(ms_from_epoch):
    """Format date time from time from epoch to human readable"""

    # get time in UTC
    datetime_in_utc = datetime.utcfromtimestamp(ms_from_epoch / 1000.0).replace(tzinfo=pytz.utc)

    # convert UTC time to PST timezone
    tz = pytz.timezone('US/Pacific')
    datetime_local = datetime_in_utc.astimezone(tz)

    return datetime_local.strftime('%A, %B %d, %Y %H:%M %Z')


def end_time(start_time, ms_duration):
    """Returns endtime using event duration in milliseconds
    Example:
        HH:MM timezone
        16:30
    """

    end_time = start_time + datetime.timedelta(milliseconds=ms_duration)
    formatted_end_time = end_time.strfttime('%H:%M %Z')

    return formatted_end_time

# class Event(object):
# # """Parses JSON data from various sources."""

# def __init__(self, evt_id):
#     self.evt_id = evt_id
#     self.name = name
#     self.description = description
#     self.start_datetime = start_datetime
#     self.duration = duration
#     self.url = url
#     self.rsvp_num = rsvp
#     self.position


"""
class MeetupAPI(object):
    self._url = "..."

    @classmethod
    def open_events(cls, lat, lng, api_key)
        returns processed open_events
        ... meetup_api_call stuff
        return cls._sanitize_event_data(meetup_api_call_data)

    @classmethod
    def _sanitize_event_data
"""

# x = MeetupAPI()
# x.instance_method()
# MeetupAPI.class_method()

def meetup_api_call(lat, lng, api_key):
    """Uses specified parameters to make a call to the Meetup API"""

    #Search parameters
    search_radius = 2 #default distance in mile(s) from location
    search_time = ',2w' #upcoming 2 weeks
    num_of_results = 20

    payload = {'key': api_key, 
               'time': search_time, 
               'sign': 'true', 
               'photo-host': 'public',
               'lat': lat, 
               'lon': lng, 
               'radius': search_radius,
               'page': num_of_results,
               # 'text_format': 'plain',
               'status': 'upcoming'}
    url = 'https://api.meetup.com/2/open_events'

    response = requests.get(url, params=payload)
    return response.json()


def meetup_jsonify_events(data):
    """"Parses out relevant data from the Meetup API response, and 
    dumps clean event info into JSON."""
    # print data
    events_list = data['results']

    map_events = {}
    #new dictionary created for every event
    for event in events_list:
        event_dict = {}

        event_dict['name'] = event['name']
        if 'description' in event:
            event_dict['description'] = event['description']
        event_dict['time'] = convert_datetime_from_epoch(event['time'])   
        # event_dict['end_time']       
        event_dict['url'] = event['event_url']
        event_dict['rsvp_num'] = event['yes_rsvp_count']   
        event_dict['position'] = {}     
        if 'venue' in event:
            event_dict['position']['lat'] = event['venue']['lat']
            event_dict['position']['lng'] = event['venue']['lon']

        evt_id = event['id']
        map_events[evt_id] = event_dict #add each to map_events

    return map_events


# def meetup_search_event(evt_id):
#     """"Parses out relevant data from the Meetup API response, and 
#     dumps clean event info into JSON."""
