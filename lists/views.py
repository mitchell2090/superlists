# from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from  lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR
import sys

def entering_info (fctn, args=[], other=[]) :
    print('\n\nEntering function "{:s}({})" --- {}'.format(fctn, args, other), file=sys.stderr)

# Create your views here.

def home_page(request) :
#    entering_info('home_page', args=[request])
    return(render(request, 'home.html', {'form' : ItemForm(), }))

def view_list(request, list_id) :
    list_= List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST' :
        form = ItemForm(data=request.POST)
        if form.is_valid() :
            Item.objects.create(text=request.POST['text'], list=list_)
            return(redirect(list_))
    return render(request, 'list.html', {'list' : list_, 'form': form } )

def new_list(request) :
    form = ItemForm(data=request.POST)
    if (form.is_valid()) :
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list = list_)
        return  redirect(list_)
    else :
        return( render(request, 'home.html', {'form' : form} ))


