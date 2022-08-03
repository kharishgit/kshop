from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import accounts
from accounts.models import Account
from django.db.models import Q
from category.models import Category
from orders.models import Order, OrderProduct, Payment
from store.models import Product
from django.db.models import Sum
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.




def admin_panel(request):
    account=Account.objects.filter( is_superadmin=False).count()
    payment=OrderProduct.objects.filter(ordered=True).count()    
    number=OrderProduct.objects.filter(ordered=True)
    transations=Payment.objects.all()    
    user=request.user
    sum=0
    
    

    stk= Product.objects.filter(is_available = True).values('category__category_name').annotate(sum = Sum('stock'))
    
    print('aaaaaaaaaaa',stk)


    
    for x in number:
        sum+=x.product_price * x.quantity

    pro_count=Product.objects.all().count()
    income = sum-10520
    
    context={
        'account':account,
        'payment':payment,
        'income':income,
        'sum':sum,
        'pro_count':pro_count,
        'transations':transations,
        'user':user,
        'stk':stk,
        'category':category,
    }
    return render(request, 'index.html',context)



def adm_categories(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            category = Category.objects.filter(Q(category_name__icontains=keyword))
            paginator = Paginator(category,3)
            page = request.GET.get('page')
            paged_category = paginator.get_page(page)
        if not category.exists():
            messages.error(request,'No matching item found.')
            return redirect(request,'adm_categories.html')
    else:
        category = Category.objects.all().order_by('category_name')
        paginator = Paginator(category,3)
        page = request.GET.get('page')
        paged_category = paginator.get_page(page)
    context ={
        'details': paged_category,
    }
    return render(request,'adm_categories.html',context)

def adm_products(request):


    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.filter(Q(product_name__icontains=keyword))
            paginator = Paginator(product,5)
            page = request.GET.get('page')
            paged_category = paginator.get_page(page)
        if not product.exists():
            messages.error(request,'No matching item found.')
            return redirect(request,'adm_products.html')
    else:
        product = Product.objects.all().order_by('product_name')
        paginator = Paginator(product,5)
        page = request.GET.get('page')
        paged_category = paginator.get_page(page)
    context ={
        'details': paged_category,
    }
    return render(request,'adm_products.html',context)



def adm_prd_add(request):
    
    return render(request,'adm_prod_add.html')


        

def adm_prd_edit(request,id):

    data = Product.objects.get(id=id)
    if request.method == 'POST':
        data.product_name = request.POST['product_name']
        data.slug = request.POST['slug']
        data.description = request.POST['description']
        data.price = request.POST['price']
        data.stock = request.POST['stock']



        data.save()
        return redirect('adm_products')



    tbl = {
        "data": data
    }

    return render(request, 'adm_prod_edit.html',tbl)

def adm_prd_dlt(request,id):
    pro = Product.objects.get(id=id)
    pro.delete()
    return redirect('adm_products')






def adm_payments(request):
    data = OrderProduct.objects.all()
    paginator = Paginator(data,7)
    page = request.GET.get('page')
    paged_category = paginator.get_page(page)
    
    tbl = {
        "details": paged_category,
    }


    return render(request, 'adm_payments.html',tbl)

def adm_user_details(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            user = Account.objects.filter(Q(first_name__icontains=keyword))
        if not user.exists():
            messages.error(request,'No matching item found.')
            return redirect(request,'adm_user.html')
    else:
        user = Account.objects.all().order_by('first_name')
    context ={
        'details': user,
    }
    return render(request,'adm_user.html',context)


def adm_orders(request):
    data = Payment.objects.all()
    tbl = {
        "details": data
    }


    return render(request, 'adm_orders.html',tbl)

def adm_add(request):
    

    return render(request, 'adm_categories_add.html')

def adm_edit(request,id):
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


# def stock(request):
#     stk= Product.objects.get(Category__category_name='jeans')
#     print('aaaaaaaaaaa',stk.stock)
#     context = {
#         'stk':stk
#     }
#     return render(request,'index.html',context)
