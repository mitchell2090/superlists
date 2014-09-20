from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
# import unittest
# import sys

# @unittest.skip
class ItemModelTest (TestCase) :
    def test_default_text(self) :
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self) :
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self) :
        list_ = List.objects.create()
        Item.objects.create(list=list_, text = 'bla')
        with self.assertRaises(IntegrityError):
            item = Item(list=list_, text='bla')
            item.save()

    def test_can_save_same_item_to_different_lists(self) :
        lists = [ List.objects.create() for i in range(2) ]
        Item.objects.create(list=lists[0], text = 'bla')
        item = Item(list=lists[1], text = 'bla')
        try :
            item.full_clean() # should not raise.
        except ValidationError as e :
            self.fail("ValidationError exception should NOT bave been raised: {} ".format(e))

    def test_list_ordering(self) :
        list1 = List.objects.create()
        items = [ Item.objects.create(list=list1, text='item {}'.format(i)) for i in range(3)  ]
        self.assertEqual ( list(Item.objects.all()), items) 


    def test_string_representation_of_Item_object(self) :
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

class ListModelTest(TestCase) :
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{:d}/'.format(list_.id))

