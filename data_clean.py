from datetime import datetime

# class JSON_clean(object):
# 	"""Parses JSON data from various sources."""


def meetup_jsonify_events(data):
    """"Parses out relevant data from the Meetup API response, and 
    dumps clean event info into JSON."""
    print data
    events_list = data['results']

    map_events = {}
    #new dictionary created for every event
    for event in events_list:
        event_dict = {}

        event_dict['name'] = event['name']
        event_dict['description'] = event['description']
        ms_from_epoch_time = event['time']
        event_dict['time'] = datetime.fromtimestamp(ms_from_epoch_time / 1000.0).strftime('%Y-%m-%d %H:%M')
        event_dict['utc_offset'] = event['utc_offset']    
        event_dict['url'] = event['event_url']
        event_dict['rsvp_num'] = event['yes_rsvp_count']   
        event_dict['position'] = {}     
        if 'venue' in event:
            event_dict['position']['lat'] = event['venue']['lat']
            event_dict['position']['lng'] = event['venue']['lon']
        else: #check if group is the actual default location
            event_dict['position']['lat'] = event['group']['group_lat']
            event_dict['position']['lng'] = event['group']['group_lon']

        evt_id = event['id']
        map_events[evt_id] = event_dict #add each to map_events

    return map_events