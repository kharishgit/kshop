
import datetime
from email.message import EmailMessage
from http.client import HTTPResponse
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from django.template.loader import render_to_string
import razorpay
from store.models import Product


# Create your views here.

def payments(request):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    body=json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered =False, order_number = body['order_id'])
    print(body)
    payment = Payment(
        user=request.user,
        payment_id=body['razorpay_payment_id'],
        payment_method =body['payment_method'],
        amount_paid = body['amount_paid'],
        status= body['status'],
    ) 
    payment.save()
    order.payment=payment
    order.is_ordered= True
    order.save()
    

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        #Clear CartItem

        CartItem.objects.filter(user=request.user).delete()
        
        

    # mail_subject = 'Thank you for your order! Visit Again'
    # message = render_to_string('order_received_email.html', {
    #     'user': request.user,
    #     'order':order,
    # })
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()

    data ={
        'order_number':order.order_number,
        'transID':payment.payment_id
    }
    return JsonResponse(data)

    



def place_order(request,total=0,quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    print (current_user)
    cart_count = cart_items.count()
    print (cart_count)
    if cart_count <= 0:
        return redirect('store')

    grant_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2* total)/100
    grant_total = total + tax

    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            data.order_total = grant_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() 

            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d= datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save() 
            

            client = razorpay.Client(auth=("rzp_test_8Cp7O32Uej0dcj", "40KLVkv8ydiGwa5nRHGrUGJO"))
            DATA = {
                "amount": data.order_total * 100,
                "currency": "INR",
                "payment_capture": 1,
                # "receipt": "receipt#1",
                # "notes": { 
                #     "key1": "value3",
                #     "key2": "value2"
                # }
                }
            payment = client.order.create(data=DATA)
            print("*************")
            print(payment)
            print("*************")


            order = Order.objects.get(user= current_user,is_ordered=False,order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grant_total':grant_total,
                'payment': payment,
            }
            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')


def success(request):
    return render(request,'orders/success.html')