
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum

from .models import Payment
from .forms import PaymentForm

from customers.models import Customer
from orders.models import Order


# ==========================================
# ORDERS BY CUSTOMER
# ==========================================

def orders_by_customer(request):

    customer_id = request.GET.get('customer_id')

    orders = Order.objects.filter(
        customer_id=customer_id
    ).select_related(
        'customer'
    ).order_by(
        '-order_date'
    )

    data = []

    for order in orders:

        # Only active payments count as paid amount
        paid_amount = Payment.objects.filter(
            order=order,
            is_deleted=False
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        balance_amount = (
            order.total_amount - paid_amount
        )

        data.append({
            'id': order.id,
            'name': f'Order #{order.id} - {order.customer.name}',
            'customer_id': order.customer_id,
            'total_amount': float(order.total_amount),
            'paid_amount': float(paid_amount),
            'balance_amount': float(balance_amount),
        })

    return JsonResponse({
        'orders': data
    })


# ==========================================
# PAYMENT LIST
# ==========================================

def payment_list(request):

    search = request.GET.get('search', '')

    # Current Payments = active payments only
    payments = Payment.objects.filter(
        is_deleted=False
    ).select_related(
        'customer',
        'order'
    ).order_by(
        '-payment_date'
    )

    if search:

        payments = payments.filter(
            customer__name__icontains=search
        ) | payments.filter(
            payment_method__icontains=search
        )

    total_payment = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'payments/payment_list.html',
        {
            'payments': payments,
            'search': search,
            'total_payment': total_payment
        }
    )


# ==========================================
# PAYMENT HISTORY
# ==========================================

def payment_history(request):

    search = request.GET.get('search', '')

    # History = ALL payments
    # Includes active + deleted payments
    payments = Payment.objects.all().select_related(
        'customer',
        'order'
    ).order_by(
        '-payment_date'
    )

    if search:

        payments = payments.filter(
            customer__name__icontains=search
        ) | payments.filter(
            payment_method__icontains=search
        )

    total_history_amount = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'payments/payment_history.html',
        {
            'payments': payments,
            'search': search,
            'total_history_amount': total_history_amount
        }
    )


# ==========================================
# ADD PAYMENT
# ==========================================

def add_payment(request):

    # --------------------------------------
    # POST REQUEST
    # --------------------------------------

    if request.method == 'POST':

        customer_id = request.POST.get(
            'customer'
        )

        order_id = request.POST.get(
            'order'
        )

        # ----------------------------------
        # CUSTOMER VALIDATION
        # ----------------------------------

        if not customer_id:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                'Please select a customer.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # ORDER VALIDATION
        # ----------------------------------

        if not order_id:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                'Please select an order.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # GET CUSTOMER
        # ----------------------------------

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        # ----------------------------------
        # GET ORDER
        # ----------------------------------

        order = get_object_or_404(
            Order,
            id=order_id
        )

        # ----------------------------------
        # CHECK CUSTOMER-ORDER MATCH
        # ----------------------------------

        if order.customer_id != customer.id:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                'Selected order does not belong to this customer.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # PAYMENT AMOUNT
        # ----------------------------------

        amount = request.POST.get(
            'amount'
        ) or 0

        try:

            from decimal import Decimal

            amount = Decimal(
                str(amount)
            )

        except Exception:

            amount = Decimal('0')

        # ----------------------------------
        # PAYMENT AMOUNT VALIDATION
        # ----------------------------------

        if amount <= 0:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                'Payment amount must be greater than 0.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # EXISTING PAID AMOUNT
        # ----------------------------------

        # Deleted payments are NOT counted
        paid_amount = Payment.objects.filter(
            order=order,
            is_deleted=False
        ).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')

        # ----------------------------------
        # REMAINING BALANCE
        # ----------------------------------

        balance_amount = (
            order.total_amount - paid_amount
        )

        # ----------------------------------
        # ALREADY FULLY PAID
        # ----------------------------------

        if balance_amount <= 0:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                'This order is already fully paid.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # PAYMENT CANNOT EXCEED BALANCE
        # ----------------------------------

        if amount > balance_amount:

            form = PaymentForm(
                request.POST
            )

            form.add_error(
                None,
                f'Payment cannot exceed the remaining balance of ₹{balance_amount}.'
            )

            return render(
                request,
                'payments/add_payment.html',
                {
                    'form': form,
                    'customers': get_customer_data(),
                    'orders': get_order_data()
                }
            )

        # ----------------------------------
        # MAKE PAYMENT
        # ----------------------------------

        payment = Payment(
            customer=customer,
            order=order,
            amount=amount,
            payment_method=request.POST.get(
                'payment_method'
            ) or 'Cash',
            notes=request.POST.get(
                'notes'
            ) or '',
            is_deleted=False
        )

        payment.save()

        return redirect(
            'payment_list'
        )

    # --------------------------------------
    # GET REQUEST
    # --------------------------------------

    form = PaymentForm()

    return render(
        request,
        'payments/add_payment.html',
        {
            'form': form,
            'customers': get_customer_data(),
            'orders': get_order_data()
        }
    )


# ==========================================
# CUSTOMER DATA
# ==========================================

def get_customer_data():

    customers = []

    customer_queryset = Customer.objects.all().order_by(
        'name'
    )

    for customer in customer_queryset:

        customers.append({
            'id': customer.id,
            'name': customer.name
        })

    return customers


# ==========================================
# ORDER DATA
# ==========================================

def get_order_data():

    orders = []

    order_queryset = Order.objects.all().select_related(
        'customer'
    ).order_by(
        '-order_date'
    )

    for order in order_queryset:

        orders.append({
            'id': order.id,
            'name': f'Order #{order.id} - {order.customer.name}',
            'customer_id': order.customer_id
        })

    return orders


# ==========================================
# EDIT PAYMENT
# ==========================================

def edit_payment(request, id):

    payment = get_object_or_404(
        Payment,
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():

            form.save()

            return redirect(
                'payment_list'
            )

    else:

        form = PaymentForm(
            instance=payment
        )

    return render(
        request,
        'payments/edit_payment.html',
        {
            'form': form,
            'payment': payment
        }
    )


# ==========================================
# DELETE PAYMENT
# ==========================================

def delete_payment(request, id):

    payment = get_object_or_404(
        Payment,
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        # Soft Delete
        # Payment remains in Payment History
        payment.is_deleted = True
        payment.save()

        return redirect(
            'payment_list'
        )

    return render(
        request,
        'payments/delete_payment.html',
        {
            'payment': payment
        }
    )


# ==========================================
# PAYMENT DETAIL
# ==========================================

def payment_detail(request, id):

    payment = get_object_or_404(
        Payment,
        id=id
    )

    order = payment.order

    order_total = order.total_amount

    # Only active payments count
    paid_amount = Payment.objects.filter(
        order=order,
        is_deleted=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance_amount = (
        order_total - paid_amount
    )

    # --------------------------------------
    # PAYMENT STATUS
    # --------------------------------------

    if paid_amount == 0:

        payment_status = 'Pending'

    elif paid_amount >= order_total:

        payment_status = 'Paid'

    else:

        payment_status = 'Partial'

    return render(
        request,
        'payments/payment_detail.html',
        {
            'payment': payment,
            'order_total': order_total,
            'paid_amount': paid_amount,
            'balance_amount': balance_amount,
            'payment_status': payment_status
        }
    )

