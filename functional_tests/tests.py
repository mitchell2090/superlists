from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import unittest



class NewVisiterTest (StaticLiveServerTestCase) :
    def setUp(self) :
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) :
        self.browser.close()
#-----       
    def check_for_row_in_list_table(self, row_text) :
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
#-----

    def test_can_start_a_list_and_retrieve_it_later(self) :
        # Edith has heard about a to-do app.  She is obcessive: she has
        # twenty-seven already, but can't let one go by without trying it. 
        self.browser.get(self.live_server_url)
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
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, r'/lists/.+')
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

        # Now a new user, Francis, drags in.
        ## We use a new browser session to make sure that no
        ## information of Edith's is leaking into Francis's session.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the site.  There is not sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock', page_text)
        self.assertNotIn('kill a fly', page_text)

        #Francis starts a new list.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own url.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, r'/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # His item is still there; still no trace of Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self) :
        # Edith goes to the home page.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # the input box is centered.  Bully
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta =5
        )

        # she starts a new list and sees the input is nicely centered there too.
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta =5
        )
        
