from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum

from .models import Order, OrderItem
from .forms import OrderItemForm
from customers.models import Customer
from products.models import Product
from payments.models import Payment
                                                                                                                                    

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors



def update_order_total(order):

    total = sum(
        item.quantity * item.price
        for item in order.items.all()
    )

    order.total_amount = total

    order.save(
        update_fields=['total_amount']
    )


def order_list(request):

    search = request.GET.get(
        'search',
        ''
    )

    orders = Order.objects.all().order_by(
        '-order_date'
    )

    if search:

        orders = orders.filter(
            customer__name__icontains=search
        ) | orders.filter(
            status__icontains=search
        )

    return render(
        request,
        'orders/order_list.html',
        {
            'orders': orders,
            'search': search
        }
    )


def add_order(request):

    if request.method == 'POST':

        customer_id = request.POST.get(
            'customer'
        )

        if not customer_id:

            return render(
                request,
                'orders/add_order.html',
                {
                    'customers': Customer.objects.all().order_by('name'),
                    'error': 'Please select a customer.'
                }
            )

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        description = request.POST.get(
            'description',
            ''
        )

        total_amount = request.POST.get(
            'total_amount'
        ) or 0

        status = request.POST.get(
            'status'
        ) or 'Pending'

        Order.objects.create(
            customer=customer,
            description=description,
            total_amount=total_amount,
            status=status
        )

        return redirect(
            'order_list'
        )

    customers = Customer.objects.all().order_by(
        'name'
    )

    return render(
        request,
        'orders/add_order.html',
        {
            'customers': customers
        }
    )


def edit_order(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    item = order.items.first()

    if request.method == 'POST':

        # =========================
        # CUSTOMER
        # =========================

        customer_name = request.POST.get(
            'customer_name',
            ''
        ).strip()

        if not customer_name:

            return render(
                request,
                'orders/edit_order.html',
                {
                    'order': order,
                    'customers': Customer.objects.all().order_by('name'),
                    'products': Product.objects.all().order_by('name'),
                    'item': item,
                    'error': 'Please enter customer name.'
                }
            )

        customer = Customer.objects.filter(
            name__iexact=customer_name
        ).first()

        if not customer:

            customer = Customer.objects.create(
                name=customer_name,
                phone=''
            )

        order.customer = customer

        # =========================
        # ORDER DETAILS
        # =========================

        order.description = request.POST.get(
            'description',
            ''
        )

        order.status = request.POST.get(
            'status',
            'Pending'
        )

        # =========================
        # PRODUCT
        # =========================

        product_id = request.POST.get(
            'product'
        )

        # =========================
        # QUANTITY
        # =========================

        quantity = request.POST.get(
            'quantity'
        )

        # =========================
        # UPDATE ORDER ITEM
        # =========================

        if product_id:

            product = get_object_or_404(
                Product,
                id=product_id
            )

            if item:

                item.product = product

                item.quantity = int(
                    quantity or 1
                )

                # Product price automatic
                item.price = product.price

                item.save()

            else:

                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(quantity or 1),
                    price=product.price
                )

            # Automatic Order Total
            update_order_total(order)

        else:

            order.total_amount = request.POST.get(
                'total_amount'
            ) or 0

            order.save()

        return redirect(
            'order_detail',
            id=order.id
        )

    # =========================
    # GET REQUEST
    # =========================

    customers = Customer.objects.all().order_by(
        'name'
    )

    products = Product.objects.all().order_by(
        'name'
    )

    return render(
        request,
        'orders/edit_order.html',
        {
            'order': order,
            'customers': customers,
            'products': products,
            'item': item
        }
    )


def delete_order(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == 'POST':

        order.delete()

        return redirect(
            'order_list'
        )

    return render(
        request,
        'orders/delete_order.html',
        {
            'order': order
        }
    )


def add_order_item(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':

        form = OrderItemForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.order = order

            # Product price automatic
            item.price = item.product.price

            item.save()

            update_order_total(
                order
            )

            return redirect(
                'order_list'
            )

    else:

        form = OrderItemForm()

    return render(
        request,
        'orders/add_order_item.html',
        {
            'form': form,
            'order': order
        }
    )


def edit_order_item(request, id):

    item = get_object_or_404(
        OrderItem,
        id=id
    )

    if request.method == 'POST':

        form = OrderItemForm(
            request.POST,
            instance=item
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            # Product price automatic
            item.price = item.product.price

            item.save()

            update_order_total(
                item.order
            )

            return redirect(
                'order_list'
            )

    else:

        form = OrderItemForm(
            instance=item
        )

    return render(
        request,
        'orders/edit_order_item.html',
        {
            'form': form,
            'item': item
        }
    )


def delete_order_item(request, id):

    item = get_object_or_404(
        OrderItem,
        id=id
    )

    if request.method == 'POST':

        order = item.order

        item.delete()

        update_order_total(
            order
        )

        return redirect(
            'order_list'
        )

    return render(
        request,
        'orders/delete_order_item.html',
        {
            'item': item
        }
    )


def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    paid_amount = Payment.objects.filter(
        order=order
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance_amount = (
        order.total_amount - paid_amount
    )

    if paid_amount == 0:

        payment_status = 'Pending'

    elif paid_amount >= order.total_amount:

        payment_status = 'Paid'

    else:

        payment_status = 'Partial'

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'paid_amount': paid_amount,
            'balance_amount': balance_amount,
            'payment_status': payment_status
        }
    )


# ==================================================
# INVOICE PDF
# ==================================================

def order_invoice(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    # =========================
    # PAYMENT CALCULATION
    # =========================

    paid_amount = Payment.objects.filter(
        order=order
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance_amount = (
        order.total_amount - paid_amount
    )

    if paid_amount == 0:

        payment_status = 'Pending'

    elif paid_amount >= order.total_amount:

        payment_status = 'Paid'

    else:

        payment_status = 'Partial'

    # =========================
    # PDF RESPONSE
    # =========================

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'inline; filename="invoice_order_{order.id}.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    # =========================
    # HEADER
    # =========================

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.rect(
        0,
        height - 100,
        width,
        100,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        colors.white
    )

    pdf.setFont(
        'Helvetica-Bold',
        24
    )

    pdf.drawString(
        50,
        height - 45,
        'SMART BOUTIQUE'
    )

    pdf.setFont(
        'Helvetica',
        11
    )

    pdf.drawString(
        50,
        height - 65,
        'Smart Tailoring & Boutique'
    )

    # =========================
    # INVOICE TITLE
    # =========================

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.setFont(
        'Helvetica-Bold',
        20
    )

    pdf.drawRightString(
        width - 50,
        height - 135,
        'INVOICE'
    )

    pdf.setFont(
        'Helvetica-Bold',
        12
    )

    pdf.drawRightString(
        width - 50,
        height - 155,
        f'#{order.id}'
    )

    # =========================
    # CUSTOMER DETAILS
    # =========================

    y = height - 140

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.setFont(
        'Helvetica-Bold',
        12
    )

    pdf.drawString(
        50,
        y,
        'CUSTOMER DETAILS'
    )

    pdf.setStrokeColor(
        colors.HexColor('#dddddd')
    )

    pdf.line(
        50,
        y - 8,
        width - 50,
        y - 8
    )

    y -= 35

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        'Helvetica-Bold',
        10
    )

    pdf.drawString(
        50,
        y,
        'Customer:'
    )

    pdf.setFont(
        'Helvetica',
        10
    )

    pdf.drawString(
        125,
        y,
        str(order.customer.name)
    )

    pdf.setFont(
        'Helvetica-Bold',
        10
    )

    pdf.drawString(
        350,
        y,
        'Order Date:'
    )

    pdf.setFont(
        'Helvetica',
        10
    )

    pdf.drawString(
        420,
        y,
        order.order_date.strftime('%d-%m-%Y')
    )

    # =========================
    # PRODUCT TABLE
    # =========================

    y -= 55

    table_left = 50
    table_right = width - 50

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.rect(
        table_left,
        y - 20,
        table_right - table_left,
        25,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        colors.white
    )

    pdf.setFont(
        'Helvetica-Bold',
        10
    )

    pdf.drawString(
        60,
        y - 11,
        'PRODUCT'
    )

    pdf.drawString(
        300,
        y - 11,
        'QTY'
    )

    pdf.drawString(
        365,
        y - 11,
        'PRICE'
    )

    pdf.drawString(
        455,
        y - 11,
        'TOTAL'
    )

    # =========================
    # TABLE ITEMS
    # =========================

    y -= 45

    pdf.setFont(
        'Helvetica',
        10
    )

    items = order.items.all()

    for item in items:

        item_total = item.quantity * item.price

        pdf.setStrokeColor(
            colors.HexColor('#dddddd')
        )

        pdf.line(
            table_left,
            y - 8,
            table_right,
            y - 8
        )

        pdf.setFillColor(
            colors.black
        )

        pdf.drawString(
            60,
            y,
            str(item.product.name)
        )

        pdf.drawString(
            300,
            y,
            str(item.quantity)
        )

        pdf.drawString(
            365,
            y,
            f'Rs. {item.price:.2f}'
        )

        pdf.drawString(
            455,
            y,
            f'Rs. {item_total:.2f}'
        )

        y -= 30

    # =========================
    # TOTAL SECTION
    # =========================

    y -= 15

    pdf.setStrokeColor(
        colors.HexColor('#5b3a29')
    )

    pdf.line(
        300,
        y,
        table_right,
        y
    )

    y -= 30

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.setFont(
        'Helvetica-Bold',
        12
    )

    pdf.drawString(
        350,
        y,
        'ORDER TOTAL:'
    )

    pdf.drawString(
        455,
        y,
        f'Rs. {order.total_amount:.2f}'
    )

    # =========================
    # PAYMENT SUMMARY
    # =========================

    y -= 55

    pdf.setFillColor(
        colors.HexColor('#5b3a29')
    )

    pdf.setFont(
        'Helvetica-Bold',
        12
    )

    pdf.drawString(
        50,
        y,
        'PAYMENT SUMMARY'
    )

    y -= 30

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        'Helvetica',
        10
    )

    pdf.drawString(
        350,
        y,
        'Paid Amount:'
    )

    pdf.drawString(
        455,
        y,
        f'Rs. {paid_amount:.2f}'
    )

    y -= 25

    pdf.drawString(
        350,
        y,
        'Balance:'
    )

    pdf.drawString(
        455,
        y,
        f'Rs. {balance_amount:.2f}'
    )

    y -= 25

    pdf.drawString(
        350,
        y,
        'Status:'
    )

    # =========================
    # PAYMENT STATUS COLOR
    # =========================

    if payment_status == 'Paid':

        status_color = colors.HexColor(
            '#2e7d32'
        )

    elif payment_status == 'Partial':

        status_color = colors.HexColor(
            '#b8860b'
        )

    else:

        status_color = colors.HexColor(
            '#8b3a32'
        )

    pdf.setFillColor(
        status_color
    )

    pdf.setFont(
        'Helvetica-Bold',
        10
    )

    pdf.drawString(
        455,
        y,
        payment_status
    )

    # =========================
    # FOOTER
    # =========================

    pdf.setStrokeColor(
        colors.HexColor('#dddddd')
    )

    pdf.line(
        50,
        70,
        width - 50,
        70
    )

    pdf.setFillColor(
        colors.HexColor('#777777')
    )

    pdf.setFont(
        'Helvetica-Oblique',
        9
    )

    pdf.drawCentredString(
        width / 2,
        50,
        'Thank you for choosing Smart Boutique!'
    )

    pdf.drawCentredString(
        width / 2,
        35,
        'Smart Tailoring & Boutique Management System'
    )

    # =========================
    # SAVE PDF
    # =========================

    pdf.save()

    return response

