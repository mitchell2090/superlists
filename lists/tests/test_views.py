from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
#import unittest
#import sys

# @unittest.skip
class ListViewTest (TestCase) :
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        test_texts=[ 'first item', 'second item']
        for text in test_texts :
            Item.objects.create(text=text, list=list_ )
        response = self.client.get('/lists/{:d}/'.format(list_.id))
        for text in test_texts :
            self.assertContains( response, text)

    def test_displays_only_items_for_that_list(self) :
        test_texts = ['first item', 'second item']
        lists = {'correct_' : List.objects.create(), 'other_' : List.objects.create() }
        for text in test_texts :
            for k in lists :
                Item.objects.create(text = k + text, list = lists[k])
        response = self.client.get('/lists/%d/' % (lists['correct_'].id,))
        for text in test_texts :
            self.assertContains(response, 'correct_'+ text)
        self.assertNotContains(response, 'other')

    def test_passes_correct_list_to_template(self) :
        lists =  { x: List.objects.create()  for x in ['current_', 'other_'] }
        response = self.client.get('/lists/{:d}/'.format(lists['current_'].id))

        self.assertEqual(response.context['list'], lists['current_'])

# @unittest.skip('omitting Browser tests')
class HomePageTest(TestCase) :

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'item_text' : 'A new list item'})

        self.assertEqual(response.content.decode(), expected_html)


# @unittest.skip
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
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/{:d}/'.format(list_.id))

class NewItemTest (TestCase) :

 
    def test_can_save_a_POST_request_to_an_existing_list(self):
        lists = { x : List.objects.create() for x in ['correct_', 'other_']}
        test_text = "New item for existing list"

        self.client.post(
            '/lists/{:d}/add_item'.format(lists['correct_'].id),
            data = {'item_text': test_text}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)
        self.assertEqual(new_item.list, lists['correct_'])
        

    def test_redirects_to_list_view(self) :
        test_text = 'test redirect to list'
        lists = { x : List.objects.create() for x in ['correct_', 'other_']}
        list_url = '/lists/{:d}/'.format(lists['correct_'].id)
        post_url = list_url + 'add_item'
        response = self.client.post( post_url, data = {'item_text' : test_text} )
        self.assertRedirects(response, list_url)
