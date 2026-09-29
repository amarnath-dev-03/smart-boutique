

from django.core.serializers import python
from django.shortcuts import render, redirect
from django.db import models
from .models import Customer
from .forms import CustomerForm


def customer_list(request):
    search = request.GET.get('search', '')

    customers = Customer.objects.all()

    if search:
        customers = customers.filter(
            models.Q(name__icontains=search) |
            models.Q(phone__icontains=search) |
            models.Q(email__icontains=search)
        )

    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'search': search
    })


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'customers/add_customer.html', {
        'form': form
    })




def edit_customer(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/add_customer.html', {
        'form': form
    })


def view_customer(request, id):
    customer = Customer.objects.get(id=id)

    return render(request, 'customers/view_customer.html', {
        'customer': customer
    })




def delete_customer(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customers/delete_customer.html', {
        'customer': customer
    })

