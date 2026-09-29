from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.order_list,
        name='order_list'
    ),

    path(
        'add/',
        views.add_order,
        name='add_order'
    ),

    path(
        'edit/<int:id>/',
        views.edit_order,
        name='edit_order'
    ),

    path(
        'delete/<int:id>/',
        views.delete_order,
        name='delete_order'
    ),

    # Order Details
    path(
        'detail/<int:id>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        'invoice/<int:id>/', 
        views.order_invoice,
        name='order_invoice'),

    # Add Order Item
    path(
        '<int:order_id>/items/add/',
        views.add_order_item,
        name='add_order_item'
    ),

    # Edit Order Item
    path(
        'items/edit/<int:id>/',
        views.edit_order_item,
        name='edit_order_item'
    ),

    # Delete Order Item
    path(
        'items/delete/<int:id>/',
        views.delete_order_item,
        name='delete_order_item'
    ),

    path(
     'invoice/<int:id>/',
     views.order_invoice,
     name='order_invoice'
    ),


]