#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest



class UseBrowserInTest   (unittest.TestCase):
    def setUp(self) :
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) :
        self.browser.close()


class NewVisitorTest   ( UseBrowserInTest) :

    def check_for_row_in_list_table(self, row_text) :
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self) :
        # Edith has heard about a to-do app.  She is obcessive: she has
        # twenty-seven already, but can't let one go by without trying it. 
        self.browser.get('http://localhost:8000')
        # She notices that the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
            

        # She types "Go to zoo to pull feathers from peacock"
        first_item = 'Go to zoo to pull feathers from peacock'
        inputbox.send_keys(first_item)

        # When she hits enter, the page updates and now the page
        # lists "1: "Go to zoo to pull feathers from peacock" as an
        # item in a TO-Do list.  
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: ' + first_item)

        # There is still a text box inviting her to add another item.  She
        # enters "Use peacock feathers to kill a fly".  (She's not a
        # fisherman.)
        second_item = 'Use peacock feathers to kill a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(second_item)

        # The page updates again and now shows both items on her list.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: ' + first_item)
        self.check_for_row_in_list_table('2: ' + second_item)

    # Edith wonders if the site will remember her. She sees that the site
    # has generated a unique URL for her:  There is explainatory text to
    # that effect.
    

    # She visits the URL --- her list is there.

    # So she goes out drinking.
        self.fail('finish the test!')    

if __name__ == '__main__' :
    unittest.main(warnings='ignore')
