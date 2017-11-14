from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class TestSearch(unittest.TestCase):
	"""Test the flow of operations with unit tests"""

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_title(self):
		self.browser.get('http://localhost:5000/')
		self.assertEqual(self.browser.title, 'blockparty homepage')

	def test_primary_address_search(self):
		self.browser.get('http://localhost:5000/')

		search_box = self.browser.find_element_by_id('pac-input')
		search_box.send_keys('450 sutter st. san francisco' + Keys.RETURN)

		result = self.browser. #saved location object is
		self.assertEqual(result, )
