# from django.http import HttpResponse
from django.shortcuts import redirect, render
from  lists.models import Item, List
import sys

# Create your views here.

def home_page(request) :
#    print('enter home_page(request = {})'.format(request))
    return render(request, 'home.html')

def view_list(request, list_id) :
#    print('enter view_list({}, list_id = {})'.format( request, list_id))
    list_= List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items' : items})

def new_list(request) :
#   print('enter new_list(request = {})'.format( request, ))
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = list_)
    return(redirect('/lists/{:d}/'.format(list_.id)))

