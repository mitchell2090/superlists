from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from .models import Item, List
import unittest
import sys
class ListViewTest (TestCase) :
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        test_texts=[ 'first item', 'second item']
        for text in test_texts :
            Item.objects.create(text=text, list=list_ )
    
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

class ItemModelTest (TestCase) :
    def test_saving_and_retrieving_items(self):
        texts = ['The first (ever) item', 'Item the second']
        list_ = List.objects.create()
        for text in texts :
            Item.objects.create(text = text, list = list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        for n in range(2) :
            self.assertEqual(saved_items[n].text, texts[n])


class NewListTest(TestCase) :

    def test_home_page_can_save_a_POST_request(self):
        test_text = 'A new list item' 
        self.client.post('/lists/new', data = { 'item_text': test_text })
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)

    def test_home_page_redirects_after_POST(self) :
        test_text = 'A new list item'
        response = self.client.post( '/lists/new', data = {'item_text' : test_text})
        self.assertRedirects(response, '/lists/the-only-list/')

