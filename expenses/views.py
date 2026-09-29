
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Expense
from .forms import ExpenseForm


@login_required(login_url='/login/')
def expense_list(request):

    search = request.GET.get('search', '').strip()

    expenses = Expense.objects.all().order_by('-created_at')

    if search:
        expenses = expenses.filter(
            Q(title__icontains=search) |
            Q(category__icontains=search) |
            Q(description__icontains=search)
        )

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses,
            'search': search
        }
    )


@login_required(login_url='/login/')
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('expense_list')

    else:

        form = ExpenseForm()

    return render(
        request,
        'expenses/add_expense.html',
        {
            'form': form
        }
    )


@login_required(login_url='/login/')
def expense_detail(request, id):

    expense = get_object_or_404(
        Expense,
        id=id
    )

    return render(
        request,
        'expenses/expense_detail.html',
        {
            'expense': expense
        }
    )


@login_required(login_url='/login/')
def edit_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()
            return redirect('expense_list')

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        'expenses/edit_expense.html',
        {
            'form': form,
            'expense': expense
        }
    )


@login_required(login_url='/login/')
def delete_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id
    )

    if request.method == 'POST':

        expense.delete()

        return redirect('expense_list')

    return render(
        request,
        'expenses/delete_expense.html',
        {
            'expense': expense
        }
    )

