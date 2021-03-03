from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm

def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        'title': title,
    }
    return render(request, 'home.html', context)

def list_items(request):
    header = 'List of list items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all() 
    context = {
                    "form": form,
                    "header": header,
                    "queryset": queryset,
        }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )
        context = {
                    "form": form,
                    "header": header,
                    "queryset": queryset,
        }
    return render(request, 'list_items.html', context)

    
def add_item(request):
    title = 'Add item'
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'add_item.html', context)