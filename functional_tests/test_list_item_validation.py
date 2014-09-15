from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class ItemValidationTest(FunctionalTest) :        

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to add an empty item.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        # After she hits enter, she sees an error message saying it cann't be blank.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # She tries again, with a nonblank message, and it works.
        self.browser.find_element_by_id('id_new_item').send_keys('buy milk\n')
        self.check_for_row_in_list_table('1: buy milk')

        # Perversely, she tries another blank item.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        
        # She sees a similar error.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # and can fix it by entering non-blank text.
        self.browser.find_element_by_id('id_new_item').send_keys(' make tea\n')
        self.check_for_row_in_list_table('2: make tea')

