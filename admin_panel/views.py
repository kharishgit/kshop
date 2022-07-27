from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from accounts.models import Account

from category.models import Category
from orders.models import Payment
from store.models import Product


# Create your views here.




def admin_panel(request):
    return render(request, 'index.html')



def adm_categories(request):
    data = Category.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_categories.html',tbl)

def adm_products(request):
    data = Product.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_products.html',tbl)


def adm_payments(request):
    data = Payment.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_payments.html',tbl)

def adm_user_details(request):
    data = Account.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_user.html',tbl)


def adm_orders(request):
    data = Account.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_orders.html',tbl)

def adm_add(request,id):
    data = Category.objects.get(id=id)
    if request.method == 'POST':
        data.category_name = request.POST['category_name']
        data.slug = request.POST['slug']
        data.description = request.POST['description']
        data.save()
        return redirect('adm_categories')



    tbl = {
        "data": data
    }

    return render(request, 'adm_categories_edit.html',tbl)

def adm_edit(request):
    pass

def adm_delete(request,id):
    cat = Category.objects.get(id=id)
    cat.delete()
    return redirect('adm_categories')

    

def adm_change_status(request,id):
    user = Account.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect('adm_user_details')
    else:
        user.is_active = True
        user.save()
        return redirect('adm_user_details')

    

