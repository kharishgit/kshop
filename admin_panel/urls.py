from django.urls import path
from . import views


urlpatterns =[
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('adm_categories/',views.adm_categories,name='adm_categories'),
    path('adm_products/',views.adm_products,name='adm_products'),
    path('adm_payments/',views.adm_payments,name='adm_payments'),
    path('adm_user_details/',views.adm_user_details,name='adm_user_details'),
    path('adm_orders/',views.adm_orders,name='adm_orders'),
    path('adm_add/<int:id>', views.adm_add,name='adm_add'),
    path('adm_delete/<int:id>', views.adm_delete,name='adm_delete'),
    path('adm_edit/<int:id>', views.adm_edit,name='adm_edit'),
    path('adm_change_status/<int:id>', views.adm_change_status,name='adm_change_status'),

]
