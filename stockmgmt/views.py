from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv

from .models import Stock, Category
from .forms import *
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
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value())
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

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
        messages.success(request, 'Successfully Saved')
        return redirect('list_items')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'add_item.html', context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Update Records')
            return redirect('/list_items')
    context = {'form':form}
    return render(request, 'add_item.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')

def list_category(request):
    header = 'List of Category'
    form = CategoryCreateForm(request.POST or None)
    queryset = Category.objects.all() 
    context = {
                    "form": form,
                    "header": header,
                    "queryset": queryset,
        }
    if request.method == 'POST':
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value())
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

        context = {
                    "form": form,
                    "header": header,
                    "queryset": queryset,
        }
    return render(request, 'list_category.html', context)

def add_category(request):
    title = 'Add Category'
    context = {
    'title': title,
    }
    
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_category')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'add_category.html', context)

    
def delete_category(request, pk):
    queryset = Category.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_category')
    return render(request, 'delete_items.html')

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity
#		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
#		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_item.html", context)


def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
#			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_item.html", context)
