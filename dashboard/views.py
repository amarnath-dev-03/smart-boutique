from django.shortcuts import render
from django.db import models
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from customers.models import Customer
from orders.models import Order
from inventory.models import InventoryItem
from payments.models import Payment
from measurements.models import Measurement
from products.models import Product
from expenses.models import Expense


@login_required(login_url='/login/')
def home(request):

    # =========================
    # BASIC COUNTS
    # =========================

    customer_count = Customer.objects.count()

    order_count = Order.objects.count()

    inventory_count = InventoryItem.objects.count()

    measurement_count = Measurement.objects.count()

    product_count = Product.objects.count()


    # =========================
    # PAYMENT TOTAL
    # Only ACTIVE payments
    # =========================

    payment_total = Payment.objects.filter(
        is_deleted=False
    ).aggregate(
        total=models.Sum('amount')
    )['total'] or 0


    # =========================
    # EXPENSE TOTAL
    # =========================

    expense_total = Expense.objects.aggregate(
        total=models.Sum('amount')
    )['total'] or 0


    # =========================
    # NET AMOUNT
    # Payments - Expenses
    # =========================

    net_amount = payment_total - expense_total


    # =========================
    # ORDER TOTAL
    # =========================

    order_total = Order.objects.aggregate(
        total=models.Sum('total_amount')
    )['total'] or 0


    # =========================
    # BALANCE
    # =========================

    balance_amount = order_total - payment_total


    # =========================
    # PAYMENT STATUS
    # =========================

    if payment_total == 0:

        payment_status = 'Pending'

    elif payment_total >= order_total:

        payment_status = 'Paid'

    else:

        payment_status = 'Partial'


    # =========================
    # ORDER STATUS COUNTS
    # =========================

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    processing_orders = Order.objects.filter(
        status='Processing'
    ).count()

    completed_orders = Order.objects.filter(
        status='Completed'
    ).count()

    cancelled_orders = Order.objects.filter(
        status='Cancelled'
    ).count()


    # =========================
    # RECENT ORDERS
    # Latest 5 Orders
    # =========================

    recent_orders = Order.objects.select_related(
        'customer'
    ).order_by(
        '-order_date'
    )[:5]


    # =========================
    # LOW STOCK ALERT
    # Stock quantity <= 5
    # Latest 5 low stock items
    # =========================

    low_stock_items = InventoryItem.objects.filter(
        quantity__lte=5
    ).order_by(
        'quantity'
    )[:5]


    # =========================
    # MONTHLY ORDERS
    # =========================

    monthly_orders = (
        Order.objects
        .annotate(
            month=TruncMonth('order_date')
        )
        .values('month')
        .annotate(
            total=models.Count('id')
        )
        .order_by('month')
    )


    # =========================
    # MONTHLY PAYMENTS
    # Only ACTIVE payments
    # =========================

    monthly_payments = (
        Payment.objects
        .filter(
            is_deleted=False
        )
        .annotate(
            month=TruncMonth('payment_date')
        )
        .values('month')
        .annotate(
            total=models.Sum('amount')
        )
        .order_by('month')
    )


    # =========================
    # MONTHLY EXPENSES
    # =========================

    monthly_expenses = (
        Expense.objects
        .annotate(
            month=TruncMonth('expense_date')
        )
        .values('month')
        .annotate(
            total=models.Sum('amount')
        )
        .order_by('month')
    )


    # =========================
    # DASHBOARD
    # =========================

    return render(
        request,
        'dashboard/home.html',
        {

            # Basic Counts
            'customer_count': customer_count,
            'order_count': order_count,
            'inventory_count': inventory_count,
            'measurement_count': measurement_count,
            'product_count': product_count,

            # Financial Data
            'payment_total': payment_total,
            'expense_total': expense_total,
            'net_amount': net_amount,
            'order_total': order_total,
            'balance_amount': balance_amount,
            'payment_status': payment_status,

            # Order Status
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,

            # Recent Orders
            'recent_orders': recent_orders,

            # Low Stock Alert
            'low_stock_items': low_stock_items,

            # Monthly Chart Data
            'monthly_orders': monthly_orders,
            'monthly_payments': monthly_payments,
            'monthly_expenses': monthly_expenses,

        }
    )
