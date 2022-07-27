from base64 import urlsafe_b64encode
from email.message import EmailMessage
import http
import random
from django.contrib import messages,auth
from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order

from .models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })   
            to_mail = email
            send_mail = EmailMessage(mail_subject, message,to = [to_mail])
            send_mail.send()
            messages.success(request,'Registration successful')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form= RegistrationForm()
    context = {
        'form': form,
     }

    return render(request,'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_admin:
            
            auth.login(request, user)
            return redirect('admin_panel')

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id= _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save() 


            except:
                pass



            auth.login(request,user)
            messages.success(request,'You are Logged in.')

            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are now logged out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation Link')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count,
    }
    return render(request,'accounts/dashboard.html',context)


def otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('mobile')
        otp =str(random.randint(1000,9999))

    return render(request,'accounts/otp.html')

def send_otp(mobile,otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    headers = { 'Content-Type': "application/json" }
    #url = "http://control.msg91.com/api/sendotp.php?otp"+otp+'&sender=ABC&message='+' Your OTP is '+'mobile'+'&authkey='+authkey+'country=91',headers=headers
    #conn.request("GET",url,headers=headers)
    res=conn.getresponse()
    data=res.read()

def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {'orders':orders}
    return render(request,'accounts/my_orders.html',context)



    