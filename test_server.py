import server
import unittest
import api_data_handler


class MyAppIntegrationTestCase(unittest.TestCase):

	def setUp(self):
		"""Done before every test"""
		
		print "(setUp ran)"
		self.client = server.app.test_client()
		server.app.config['TESTING'] = True


		def _mock_meetup_api_call(lat, lng, api_key):
			"""Fake external API call"""

			return {u'meta': {u'count': 1, u'updated': 1507680583782, u'description': u"Searches for recent and upcoming public events hosted by Meetup groups. Its search window  is the past one month through the next three months, and is subject to change. Open Events is optimized to search for current events by location, category, topic, or text, and only lists Meetups that have **3 or more RSVPs**. The number or results returned with each request is not guaranteed to be the same as the page size due to secondary filtering. If you're looking for a particular event or events within a particular group, use the standard [Events](/meetup_api/docs/2/events/) method.", u'title': u'Meetup Open Events v2', u'url': u'https://api.meetup.com/2/open_events?and_text=False&offset=0&sign=True&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&key=4c711382b2570616b48624d3838582&desc=False&status=upcoming', u'total_count': 571, u'lon': -122.4239528, u'next': u'https://api.meetup.com/2/open_events?and_text=False&offset=1&sign=True&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&key=4c711382b2570616b48624d3838582&desc=False&status=upcoming', u'signed_url': u'https://api.meetup.com/2/open_events?and_text=False&offset=0&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&desc=False&status=upcoming&sig_id=17020591&sig=e6ba8a0e87b06444003be84c821b2cba2b6e1327', u'lat': 37.7970106, u'link': u'https://api.meetup.com/2/open_events', u'id': u'', u'method': u'OpenEvents'}, u'results': [{u'status': u'upcoming', u'distance': 1.458785891532898, u'utc_offset': -25200000, u'event_url': u'https://www.meetup.com/Developing-with-Data-in-San-Francisco/events/243625539/', u'group': {u'who': u'Developers', u'name': u'Developing with Data in San Francisco', u'group_lat': 37.77000045776367, u'created': 1339100460000, u'join_mode': u'open', u'group_lon': -122.41000366210938, u'urlname': u'Developing-with-Data-in-San-Francisco', u'id': 4027502}, u'description': u'<p>Were excited to partner with BoxWorks and offer discounted tickets to their upcoming conference in SF to the members of our community.</p> <p>BoxWorks will be from October 10th - 12th at Moscone Center West in San Francisco. Here are some of the highlights:<br/>- 20+ developer breakout sessions.<br/>- Keynote speakers like Dr. Neil deGrasse Tyson, Kevin Scott, Valerie Jarrett, and more.<br/>- Free developer training for BoxWorks registrants.<br/>- Dev challenges to win amazing prizes.<br/>- Developer happy hour featuring some visionary speakers.<br/>- An awesome BoxWorks after party. Previous bands we\'ve had play were Beck, Jimmy Eat World, and Blink 182</p> <p>To take advantage of the discount, head over to the registration page (<a href="https://www.boxworksevents.com/boxworksregistrationpage" class="linkified">https://www.boxworksevents.com/boxworksregistrationpage</a>) and use code17WorksNJNI299 during checkout to drop the price down $400 to $299.</p>', u'created': 1506265963000, u'venue': {u'city': u'San Francisco', u'name': u'Moscone Center West', u'country': u'US', u'lon': -122.4039, u'localized_country_name': u'USA', u'address_1': u'800 Howard Street', u'repinned': False, u'lat': 37.783127, u'id': 25510449}, u'updated': 1506265963000, u'visibility': u'public', u'yes_rsvp_count': 4, u'time': 1507647600000, u'duration': 205200000, u'waitlist_count': 0, u'headcount': 0, u'maybe_rsvp_count': 0, u'id': u'243625539', u'name': u'BoxWorks - October 10th - 12th at Moscone Center West in San Francisco'}]}
			

		api_data_handler.meetup_api_call = _mock_meetup_api_call


	def test_index_route(self):
		"""Test '/' route works"""

		result = self.client.get('/')
		self.assertEqual(result.status_code, 200)


	def test_search_events_route(self):
		"""Test '/search-events' route works"""

		result = self.client.get('/search-events')
		self.assertEqual(result.status_code, 200)


class MyAppUnitTestCase(unittest.TestCase):
    """Unit tests: discrete code testing."""

    def test_mtup_clean_data_method(self):
		"""Tests api_data_handler.meetup_jsonify_events() with Meetup standard format."""

		raw_data = {u'meta': {u'count': 1, u'updated': 1507680583782, u'description': u"Searches for recent and upcoming public events hosted by Meetup groups. Its search window  is the past one month through the next three months, and is subject to change. Open Events is optimized to search for current events by location, category, topic, or text, and only lists Meetups that have **3 or more RSVPs**. The number or results returned with each request is not guaranteed to be the same as the page size due to secondary filtering. If you're looking for a particular event or events within a particular group, use the standard [Events](/meetup_api/docs/2/events/) method.", u'title': u'Meetup Open Events v2', u'url': u'https://api.meetup.com/2/open_events?and_text=False&offset=0&sign=True&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&key=4c711382b2570616b48624d3838582&desc=False&status=upcoming', u'total_count': 571, u'lon': -122.4239528, u'next': u'https://api.meetup.com/2/open_events?and_text=False&offset=1&sign=True&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&key=4c711382b2570616b48624d3838582&desc=False&status=upcoming', u'signed_url': u'https://api.meetup.com/2/open_events?and_text=False&offset=0&format=json&lon=-122.4239528&limited_events=False&photo-host=public&page=1&time=%2C2w&radius=2&lat=37.7970106&desc=False&status=upcoming&sig_id=17020591&sig=e6ba8a0e87b06444003be84c821b2cba2b6e1327', u'lat': 37.7970106, u'link': u'https://api.meetup.com/2/open_events', u'id': u'', u'method': u'OpenEvents'}, u'results': [{u'status': u'upcoming', u'distance': 1.458785891532898, u'utc_offset': -25200000, u'event_url': u'https://www.meetup.com/Developing-with-Data-in-San-Francisco/events/243625539/', u'group': {u'who': u'Developers', u'name': u'Developing with Data in San Francisco', u'group_lat': 37.77000045776367, u'created': 1339100460000, u'join_mode': u'open', u'group_lon': -122.41000366210938, u'urlname': u'Developing-with-Data-in-San-Francisco', u'id': 4027502}, u'description': u'<p>Were excited to partner with BoxWorks and offer discounted tickets to their upcoming conference in SF to the members of our community.</p> <p>BoxWorks will be from October 10th - 12th at Moscone Center West in San Francisco. Here are some of the highlights:<br/>- 20+ developer breakout sessions.<br/>- Keynote speakers like Dr. Neil deGrasse Tyson, Kevin Scott, Valerie Jarrett, and more.<br/>- Free developer training for BoxWorks registrants.<br/>- Dev challenges to win amazing prizes.<br/>- Developer happy hour featuring some visionary speakers.<br/>- An awesome BoxWorks after party. Previous bands we\'ve had play were Beck, Jimmy Eat World, and Blink 182</p> <p>To take advantage of the discount, head over to the registration page (<a href="https://www.boxworksevents.com/boxworksregistrationpage" class="linkified">https://www.boxworksevents.com/boxworksregistrationpage</a>) and use code17WorksNJNI299 during checkout to drop the price down $400 to $299.</p>', u'created': 1506265963000, u'venue': {u'city': u'San Francisco', u'name': u'Moscone Center West', u'country': u'US', u'lon': -122.4039, u'localized_country_name': u'USA', u'address_1': u'800 Howard Street', u'repinned': False, u'lat': 37.783127, u'id': 25510449}, u'updated': 1506265963000, u'visibility': u'public', u'yes_rsvp_count': 4, u'time': 1507647600000, u'duration': 205200000, u'waitlist_count': 0, u'headcount': 0, u'maybe_rsvp_count': 0, u'id': u'243625539', u'name': u'BoxWorks - October 10th - 12th at Moscone Center West in San Francisco'}]}
			
		clean_data = {u'243625539': {'utc_offset': -25200000, 'name': u'BoxWorks - October 10th - 12th at Moscone Center West in San Francisco', 'url': u'https://www.meetup.com/Developing-with-Data-in-San-Francisco/events/243625539/', 'rsvp_num': 4, 'time': '2017-10-10 15:00', 'position': {'lat': 37.783127, 'lng': -122.4039}, 'description': u'<p>Were excited to partner with BoxWorks and offer discounted tickets to their upcoming conference in SF to the members of our community.</p> <p>BoxWorks will be from October 10th - 12th at Moscone Center West in San Francisco. Here are some of the highlights:<br/>- 20+ developer breakout sessions.<br/>- Keynote speakers like Dr. Neil deGrasse Tyson, Kevin Scott, Valerie Jarrett, and more.<br/>- Free developer training for BoxWorks registrants.<br/>- Dev challenges to win amazing prizes.<br/>- Developer happy hour featuring some visionary speakers.<br/>- An awesome BoxWorks after party. Previous bands we\'ve had play were Beck, Jimmy Eat World, and Blink 182</p> <p>To take advantage of the discount, head over to the registration page (<a href="https://www.boxworksevents.com/boxworksregistrationpage" class="linkified">https://www.boxworksevents.com/boxworksregistrationpage</a>) and use code17WorksNJNI299 during checkout to drop the price down $400 to $299.</p>'}}
			

		self.assertEqual(api_data_handler.meetup_jsonify_events(raw_data), clean_data)


  #   def test_evtbr_clean_data_method(self):
		# """Tests api_data_handler.meetup_jsonify_events() with Meetup standard format."""

		# next

if __name__ == '__main__': 
	unittest.main()

