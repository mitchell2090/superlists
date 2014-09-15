# from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from  lists.models import Item, List
import sys

def entering_info (fctn, args=[], other=[]) :
    print('\n\nEntering function "{:s}({})" --- {}'.format(fctn, args, other), file=sys.stderr)

# Create your views here.

def home_page(request) :
#    entering_info('home_page', args=[request])
    return(render(request, 'home.html'))

def view_list(request, list_id) :
#    entering_info('view_list', args=[request, list_id])
    list_= List.objects.get(id=list_id)
    return render(request, 'list.html', {'list' : list_ })

def new_list(request) :
#    entering_info('new_list', args=[request])
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list = list_)
    try :
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return( render(request, 'home.html', {"error": error}))
    return(redirect('/lists/{}/'.format(list_.id)))


def add_item(request, list_id) :
 #   entering_info('add_item', args=[request, list_id])
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list = list_)
    return(redirect('/lists/{}/'.format(list_id)))
