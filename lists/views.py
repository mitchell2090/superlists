# from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from  lists.models import Item, List
from lists.forms import ItemForm
import sys

def entering_info (fctn, args=[], other=[]) :
    print('\n\nEntering function "{:s}({})" --- {}'.format(fctn, args, other), file=sys.stderr)

# Create your views here.

def home_page(request) :
#    entering_info('home_page', args=[request])
    return(render(request, 'home.html', {'form' : ItemForm(), }))

def view_list(request, list_id) :
    list_= List.objects.get(id=list_id)
    error = None
    if request.method == 'POST' :
        try :
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()                 # This is a change from the book. 
                                          # Without it, the empty item is entered into the list even
                                          # though the warning is given.   My conjecture is that there has
                                          # been a change, so the exception now comes in "item.save()" and not
                                          # until the item has been saved.
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list' : list_, 'error' : error })

def new_list(request) :
#    entering_info('new_list', args=[request])
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list = list_)
    try :
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return( render(request, 'home.html', {"error": error}))
    return  redirect(list_)

