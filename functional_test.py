#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3

from selenium import webdriver
import unittest



class UseBrowserInTest   (unittest.TestCase):
    def setUp(self) :
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self) :
        self.browser.quit()


class NewVisitorTest   ( UseBrowserInTest) :
    def test_can_start_a_list_and_retrieve_it_later(self) :
    # Edith has heard about a to-do app.  She is obcessive: she has
    # twenty-seven already, but can't let one go by without trying it. 

    # She notices that the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)

    # She is invited to enter a to-do item straight away.

    # She types "Steal peacock feathers"

    # When she hits enter, the page updates and now the page    lists "1: But
    # peacock feathers" as an item in a TO-Do list.

    # There is still a text box inviting her to add another item.  She
    # enters "Use peacock feathers to kill a fly".  (She's not a
    # fisherman.)

    # The page updates again and now shows both items on her list.

    # Edith wonders if the site will remember her. She sees that the site
    # has generated a unique URL for her:  There is explainatory text to
    # that effect.


    # She visits the URL --- her list is there.

    # So she goes out drinking.


if __name__ == '__main__' :
    unittest.main(warnings='ignore')
