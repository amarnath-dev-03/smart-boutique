from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required

from .models import Customer
from .forms import CustomerForm


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

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


@login_required(login_url='/login/')
def view_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    return render(request, 'customers/view_customer.html', {
        'customer': customer
    })


@login_required(login_url='/login/')
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customers/delete_customer.html', {
        'customer': customer
    })
