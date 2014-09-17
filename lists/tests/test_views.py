from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm
# from  unittest import skip
#import sys

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

#----------------------------------------------------------------
class HomePageTest(TestCase) :

    maxDiff = None


    def test_home_page_renders_home_template(self) :
            response = self.client.get('/')
            self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self) :
            response = self.client.get('/')
            self.assertIsInstance(response.context['form'], ItemForm)
                                          


#----------------------------------------------------------------

class NewListTest(TestCase) :

    def test_home_page_can_save_a_POST_request(self):
        test_text = 'A new list item' 
        self.client.post('/lists/new', data = { 'text': test_text })
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)

    def test_home_page_redirects_after_POST(self) :
        test_text = 'A new list item'
        response = self.client.post( '/lists/new', data = {'text' : test_text})
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/{:d}/'.format(list_.id))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text' : ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


    def test_invalid_list_items_arent_saved(self):
        self.client.post('lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


    def test_can_save_a_POST_request_to_an_existing_list(self):
        lists = { x : List.objects.create() for x in ['correct_', 'other_']}
        test_text = "New item for existing list"

        self.client.post(
            '/lists/{:d}/'.format(lists['correct_'].id),
            data = {'text': test_text}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)
        self.assertEqual(new_item.list, lists['correct_'])
        

    def test_POST_redirects_to_list_view(self) :
        test_text = 'test redirect to list'
        lists = { x : List.objects.create() for x in ['correct', 'other']}
        list_url = '/lists/{:d}/'.format(lists['correct'].id)
        post_url = list_url
        response = self.client.post( post_url, data = {'text' : test_text} )
        self.assertRedirects(response, list_url)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
             '/lists/{:d}/'.format(list_.id),
             data = {'text': ''}
         )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

