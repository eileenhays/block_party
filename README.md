# BlockParty: Community events aggregator 
https://blockparty-app.herokuapp.com/

Built by Eileen Hays-Schwantes

## Overview
Moved to a new city or neighborhood? Bored and want to find something random to do? Ready to expand your social network IRL? 

BlockParty is a web app that enables users to engage with their community through real social interaction with their neighbors. The user can input their address and interactively showcase events in their neighborhood on a map or listed, and save favorite events.

## Tech Stack
Backend: Python, Flask, SQLAlchemy, PostgreSQL, bcrypt (encryption)

Flask extensions: Flask-Login, Flask-SQLAlchemy

Testing: unit tests

Frontend: JavaScript, jQuery, AJAX, Jinja, HTML5, CSS3, Bootstrap

APIs: Google Maps Javascript V3, Meetup, and Eventbrite

## Views
### Homepage and Event Map
By entering their "homebase address," users search for upcoming public activities and events within their vicinity from Meetup and Eventbrite. Event details, including name, time, description, and link can be easily viewed geographically on a Google map. 

![Map of Search Events](https://j.gifs.com/zKYj72.gif)
![Event Details Pop-up](https://j.gifs.com/7LVKXB.gif)

### Community Events List
Users can also scroll down to view the same events listed and add events to Favorites.

![Events List](https://j.gifs.com/BL90no.gif)

### Favorites Page
Users can login to save and view their favorite events later, which is updated when events expire.

![Favorites Page](https://j.gifs.com/D9WDAk.gif)

## Forking Project
You need to have your own API keys for Google Maps, Meetup, and Eventbrite. 

```python
pip install -r requirements.txt
python server.py
```


