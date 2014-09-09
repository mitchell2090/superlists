from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from .models import Item
import unittest
import sys
class ListViewTest (TestCase) :
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        test_texts=[ 'first item', 'second item']
        for text in test_texts :
            Item.objects.create(text=text)
    
        response = self.client.get('/lists/the-only-list/')
        for text in test_texts :
            self.assertContains( response, text)


# @unittest.skip('omitting Browser tests')
class HomePageTest(TestCase) :

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'new_text_item' : 'A new list item'})
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        text = 'A new list item' 
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = text

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_home_page_redirects_after_POST(self) :
        test_text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = test_text

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list/')

    def test_home_page_doesnt_save_empty_items(self) :
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)



class ItemModelTest (TestCase) :
    def test_saving_and_retrieving_items(self):
        texts = ['The first (ever) item', 'Item the second']
        for text in texts :
            item = Item()
            item.text = text
            item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        for n in range(2) :
            self.assertEqual(saved_items[n].text, texts[n])
