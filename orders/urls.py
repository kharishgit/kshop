from . import views
from django.urls import path

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('success/',views.success,name='success'),




]