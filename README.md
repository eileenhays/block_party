# BlockParty: Community events aggregator 
https://blockparty-app.herokuapp.com/

Built by Eileen Hays-Schwantes

## Overview
Moved to a new city or neighborhood? Bored and want to find something random to do? Ready to expand your social network IRL? 

BlockParty is a web app that enables users to engage with their community through real social interaction with their neighbors. The user can input their address and interactively showcase dynamic events in their neighborhood on a map and save or remove favorite events.

## Tech Stack
Backend: Python, Flask, SQLAlchemy, PostgreSQL, bcrypt (encryption)

Flask extensions: Flask-Login, Flask-SQLAlchemy

Testing: unit tests

Frontend: JavaScript, jQuery, AJAX, Jinja, HTML5, CSS3, Bootstrap

APIs: Google Maps Javascript V3, Meetup, and Eventbrite

## Views
### Homepage and Event Map
By entering their "homebase address," users search for upcoming public activities and events within their vicinity from Meetup and Eventbrite. Event details, including name, time, description, and link can be easily viewed geographically on a Google map. 

![Homepage and Event Map](https://gifs.com/gif/blockparty-event-map-E9WEv4)

### Community Events List
Users can also scroll down to view the same events listed and add events to Favorites.

![Community Event List](https://gifs.com/gif/blockparty-event-list-kZXklv)

### Favorites Page
Users can login to save and view their favorite events later, which is updated when events expire.

![Favorites Page](https://gifs.com/gif/blockparty-favorites-D9WDAk)

## Forking Project
You need to have your own API keys for Google Maps, Meetup, and Eventbrite. 

```python
pip install -r requirements.txt
python server.py
```


