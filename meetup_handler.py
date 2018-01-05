from datetime import datetime
import pytz
import requests
import json
import os


class Meetup_API(object):

    MEETUP_API_KEY = os.environ.get('MEETUP_API_KEY')
    MEETUP_EVENT_URL = 'https://api.meetup.com/2/open_events'

    @classmethod
    def find_events(cls, lat, lng):
        """Uses specified parameters to make a call to the Meetup API"""

        #Search parameters
        search_radius = 2 #default distance in mile(s) from location
        search_time = ',2w' #upcoming 2 weeks
        num_of_results = 30

        payload = {'key': cls.MEETUP_API_KEY, 
                   'time': search_time, 
                   'sign': 'true', 
                   'photo-host': 'public',
                   'lat': lat, 
                   'lon': lng, 
                   'radius': search_radius,
                   'page': num_of_results,
                   'status': 'upcoming'}

        response = requests.get(cls.MEETUP_EVENT_URL, params=payload)
        return response.json()


    @classmethod    
    def sanitize_data(cls, data):
        """"Parses out relevant data from the Meetup API response, and 
        dumps clean event info into JSON."""
        # print data
        events_list = data['results']

        map_events = {}
        #new dictionary created for every event
        for event in events_list:
            event_dict = {}

            event_dict['src_evt_id'] = event['id']
            event_dict['src_id'] = 'mtup'
            event_dict['datetime'] = convert_datetime_from_epoch(event['time']) 
            # event_dict['end_time'] = end_time(event_dict['time'], event['duration']) 
            event_dict['name'] = event['name']
            if 'description' in event:
                event_dict['description'] = event['description']      
            event_dict['url'] = event['event_url']
            event_dict['group'] = event['group']['name']
            event_dict['position'] = {}     
            if 'venue' in event:
                event_dict['position']['lat'] = event['venue']['lat']
                event_dict['position']['lng'] = event['venue']['lon']
                if 'address' in event['venue']:
                    formatted_addy = event['venue']['address_1'] + event['venue']['address_2'] + event['venue']['city'] + ',' + event['venue']['state'] + event['venue']['zip']
                    event_dict['address'] = formatted_addy
                    print "\n\n\nAddress: ", event_dict['address']
            if 'category' in event['group']:
                event_dict['category'] = event['group']['category']
            evt_id = event['id']
            map_events[evt_id] = event_dict #add each to map_events


        return map_events

#static method??? 
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

## Notes if you want to init a new MeetupAPI object (for creating a new event) ###
 # x = MeetupAPI()
# x.instance_method()
# MeetupAPI.class_method()

# if __name__ == "__main__":
#   Meetup_API.find_categories()