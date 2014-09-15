from django.test import TestCase
from lists.models import Item, List
# import unittest
# import sys

# @unittest.skip
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

