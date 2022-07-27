from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('',views.dashboard,name='dashboard'),

    



    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('otp/',views.otp,name='otp'),
    path('my_orders/',views.my_orders,name='my_orders'),

    






]