from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.payment_list,
        name='payment_list'
    ),

    path(
        'add/',
        views.add_payment,
        name='add_payment'
    ),

    path(
        'detail/<int:id>/',
        views.payment_detail,
        name='payment_detail'
    ),

    path(
        'edit/<int:id>/',
        views.edit_payment,
        name='edit_payment'
    ),

    path(
        'delete/<int:id>/',
        views.delete_payment,
        name='delete_payment'
    ),

    path(
    'history/',
    views.payment_history,
    name='payment_history'
),


    path(
    'orders-by-customer/',
    views.orders_by_customer,
    name='orders_by_customer'
    ),
    

]