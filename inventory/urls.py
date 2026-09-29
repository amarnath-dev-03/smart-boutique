from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_inventory, name='add_inventory'),
    path('view/<int:id>/', views.view_inventory, name='view_inventory'),
    path('edit/<int:id>/', views.edit_inventory, name='edit_inventory'),
    path('delete/<int:id>/', views.delete_inventory, name='delete_inventory'),
]