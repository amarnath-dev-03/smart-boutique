
from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.measurement_list,
        name='measurement_list'
    ),

    path(
        'add/',
        views.add_measurement,
        name='add_measurement'
    ),

    path(
        'view/<int:id>/',
        views.view_measurement,
        name='view_measurement'
    ),

    path(
        'edit/<int:id>/',
        views.edit_measurement,
        name='edit_measurement'
    ),

    path(
        'delete/<int:id>/',
        views.delete_measurement,
        name='delete_measurement'
    ),

]

