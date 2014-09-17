#from .base import FunctionalTest
from . import base
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from sys import stderr

class ItemValidationTest(base.FunctionalTest) :        

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to add an empty item.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        # After she hits enter, she sees an error message saying it can't be blank.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # She tries again, with a nonblank message, and it works.
        self.get_item_input_box().send_keys('buy milk\n')
        self.check_for_row_in_list_table('1: buy milk')

        # Perversely, she tries another blank item.
        self.get_item_input_box().send_keys('\n')
        
        # She sees a similar error.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # and can fix it by entering non-blank text.
        self.get_item_input_box().send_keys('make tea\n')
        self.check_for_row_in_list_table('2: make tea')

