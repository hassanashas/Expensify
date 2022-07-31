from django.shortcuts import render, redirect
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator


def search_expenses(request):
    pass

def index(request):
    
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'expenses/index.html', context)

def add_expense(request):

    categories = Category.objects.all()
    context = {
        'cateogries': categories,
        'values': request.POST
    }

    if request.method == "POST":

        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        if not amount:
            messages.warning(request, "Amount can not be Empty")
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.warning(request, "Description can not be Empty")
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        messages.success(request, "Expense has been Successfully Added")
        return redirect('exp')


    return render(request, 'expenses/add_expense.html', context)


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories
    }
    if request.method == "GET":
        
        return render(request, 'expenses/edit_expense.html', context)

    else:

        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        if not amount:
            messages.warning(request, "Amount can not be Empty")
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.warning(request, "Description can not be Empty")
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.amount = amount 
        expense.description = description 
        expense.category = category 
        expense.date = date 
        expense.save() 

        messages.success(request, "Expense has been Saved Successfully")
        return redirect('exp')