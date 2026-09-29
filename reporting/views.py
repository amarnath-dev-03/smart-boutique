
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from customers.models import Customer
from products.models import Product
from orders.models import Order
from payments.models import Payment
from inventory.models import InventoryItem
from expenses.models import Expense


# =========================================================
# BUSINESS REPORT PAGE
# =========================================================

@login_required(login_url='/login/')
def report_home(request):

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    order_queryset = Order.objects.all()
    payment_queryset = Payment.objects.all()
    expense_queryset = Expense.objects.all()

    # =========================
    # DATE FILTER
    # =========================

    if from_date:

        parsed_from_date = parse_date(from_date)

        if parsed_from_date:

            order_queryset = order_queryset.filter(
                order_date__date__gte=parsed_from_date
            )

            payment_queryset = payment_queryset.filter(
                payment_date__date__gte=parsed_from_date
            )

            expense_queryset = expense_queryset.filter(
                expense_date__gte=parsed_from_date
            )

    if to_date:

        parsed_to_date = parse_date(to_date)

        if parsed_to_date:

            order_queryset = order_queryset.filter(
                order_date__date__lte=parsed_to_date
            )

            payment_queryset = payment_queryset.filter(
                payment_date__date__lte=parsed_to_date
            )

            expense_queryset = expense_queryset.filter(
                expense_date__lte=parsed_to_date
            )

    # =========================
    # BASIC COUNTS
    # =========================

    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = order_queryset.count()
    inventory_count = InventoryItem.objects.count()

    # =========================
    # FINANCIAL TOTALS
    # =========================

    total_sales = (
        order_queryset.aggregate(
            total=Sum('total_amount')
        )['total']
        or 0
    )

    total_payments = (
        payment_queryset.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    total_expenses = (
        expense_queryset.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    balance = total_sales - total_payments
    net_balance = total_sales - total_expenses

    # =========================
    # ORDER STATUS
    # =========================

    pending_orders = order_queryset.filter(
        status='Pending'
    ).count()

    processing_orders = order_queryset.filter(
        status='Processing'
    ).count()

    completed_orders = order_queryset.filter(
        status='Completed'
    ).count()

    cancelled_orders = order_queryset.filter(
        status='Cancelled'
    ).count()

    total_status_orders = (
        pending_orders
        + processing_orders
        + completed_orders
        + cancelled_orders
    )

    if total_status_orders > 0:

        pending_percent = round(
            (pending_orders / total_status_orders) * 100
        )

        processing_percent = round(
            (processing_orders / total_status_orders) * 100
        )

        completed_percent = round(
            (completed_orders / total_status_orders) * 100
        )

        cancelled_percent = round(
            (cancelled_orders / total_status_orders) * 100
        )

    else:

        pending_percent = 0
        processing_percent = 0
        completed_percent = 0
        cancelled_percent = 0

    # =========================
    # FINANCIAL PERCENTAGES
    # =========================

    financial_max = max(
        float(total_sales),
        float(total_payments),
        float(total_expenses),
        float(balance) if balance > 0 else 0,
        float(net_balance) if net_balance > 0 else 0,
        1
    )

    sales_percent = round(
        (float(total_sales) / financial_max) * 100
    )

    payments_percent = round(
        (float(total_payments) / financial_max) * 100
    )

    expenses_percent = round(
        (float(total_expenses) / financial_max) * 100
    )

    balance_percent = (
        round(
            (float(balance) / financial_max) * 100
        )
        if balance > 0
        else 0
    )

    # =========================
    # MONTHLY DATA
    # =========================

    monthly_orders_queryset = (
        order_queryset
        .annotate(
            month=TruncMonth('order_date')
        )
        .values('month')
        .annotate(
            total=Sum('total_amount')
        )
        .order_by('month')
    )

    monthly_orders = {}

    for item in monthly_orders_queryset:

        if item['month']:

            month_key = item['month'].strftime('%Y-%m')

            monthly_orders[month_key] = {
                'label': item['month'].strftime('%b %Y'),
                'sales': float(item['total'] or 0),
                'payments': 0,
                'expenses': 0,
            }

    monthly_payments_queryset = (
        payment_queryset
        .annotate(
            month=TruncMonth('payment_date')
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )

    for item in monthly_payments_queryset:

        if item['month']:

            month_key = item['month'].strftime('%Y-%m')

            if month_key not in monthly_orders:

                monthly_orders[month_key] = {
                    'label': item['month'].strftime('%b %Y'),
                    'sales': 0,
                    'payments': 0,
                    'expenses': 0,
                }

            monthly_orders[month_key]['payments'] = float(
                item['total'] or 0
            )

    monthly_expenses_queryset = (
        expense_queryset
        .annotate(
            month=TruncMonth('expense_date')
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )

    for item in monthly_expenses_queryset:

        if item['month']:

            month_key = item['month'].strftime('%Y-%m')

            if month_key not in monthly_orders:

                monthly_orders[month_key] = {
                    'label': item['month'].strftime('%b %Y'),
                    'sales': 0,
                    'payments': 0,
                    'expenses': 0,
                }

            monthly_orders[month_key]['expenses'] = float(
                item['total'] or 0
            )

    monthly_business = []

    for month_key in sorted(monthly_orders.keys()):

        sales = monthly_orders[month_key]['sales']
        payments = monthly_orders[month_key]['payments']
        expenses = monthly_orders[month_key]['expenses']

        net = sales - expenses

        monthly_business.append(
            {
                'month': month_key,
                'label': monthly_orders[month_key]['label'],
                'sales': sales,
                'payments': payments,
                'expenses': expenses,
                'net': net,
            }
        )

    monthly_values = []

    for item in monthly_business:

        monthly_values.append(item['sales'])
        monthly_values.append(item['payments'])
        monthly_values.append(item['expenses'])

    monthly_max = max(
        monthly_values + [1]
    )

    for item in monthly_business:

        item['sales_percent'] = round(
            (item['sales'] / monthly_max) * 100
        )

        item['payments_percent'] = round(
            (item['payments'] / monthly_max) * 100
        )

        item['expenses_percent'] = round(
            (item['expenses'] / monthly_max) * 100
        )

    # =========================
    # CONTEXT
    # =========================

    context = {

        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
        'inventory_count': inventory_count,

        'total_sales': total_sales,
        'total_payments': total_payments,
        'total_expenses': total_expenses,
        'balance': balance,
        'net_balance': net_balance,

        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,

        'pending_percent': pending_percent,
        'processing_percent': processing_percent,
        'completed_percent': completed_percent,
        'cancelled_percent': cancelled_percent,

        'sales_percent': sales_percent,
        'payments_percent': payments_percent,
        'expenses_percent': expenses_percent,
        'balance_percent': balance_percent,

        'monthly_business': monthly_business,

        'from_date': from_date,
        'to_date': to_date,
    }

    return render(
        request,
        'reporting/report_home.html',
        context
    )


# =========================================================
# PROFESSIONAL PDF BUSINESS REPORT
# =========================================================

@login_required(login_url='/login/')
def report_pdf(request):

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    order_queryset = Order.objects.all()
    payment_queryset = Payment.objects.all()
    expense_queryset = Expense.objects.all()

    # =========================
    # DATE FILTER
    # =========================

    if from_date:

        parsed_from_date = parse_date(from_date)

        if parsed_from_date:

            order_queryset = order_queryset.filter(
                order_date__date__gte=parsed_from_date
            )

            payment_queryset = payment_queryset.filter(
                payment_date__date__gte=parsed_from_date
            )

            expense_queryset = expense_queryset.filter(
                expense_date__gte=parsed_from_date
            )

    if to_date:

        parsed_to_date = parse_date(to_date)

        if parsed_to_date:

            order_queryset = order_queryset.filter(
                order_date__date__lte=parsed_to_date
            )

            payment_queryset = payment_queryset.filter(
                payment_date__date__lte=parsed_to_date
            )

            expense_queryset = expense_queryset.filter(
                expense_date__lte=parsed_to_date
            )

    # =========================
    # TOTALS
    # =========================

    total_sales = (
        order_queryset.aggregate(
            total=Sum('total_amount')
        )['total']
        or 0
    )

    total_payments = (
        payment_queryset.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    total_expenses = (
        expense_queryset.aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    pending_balance = total_sales - total_payments
    net_balance = total_sales - total_expenses

    # =========================
    # COUNTS
    # =========================

    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = order_queryset.count()
    inventory_count = InventoryItem.objects.count()

    # =========================
    # ORDER STATUS
    # =========================

    pending_orders = order_queryset.filter(
        status='Pending'
    ).count()

    processing_orders = order_queryset.filter(
        status='Processing'
    ).count()

    completed_orders = order_queryset.filter(
        status='Completed'
    ).count()

    cancelled_orders = order_queryset.filter(
        status='Cancelled'
    ).count()

    # =========================
    # MONTHLY DATA
    # =========================

    monthly_orders = {}

    monthly_sales = (
        order_queryset
        .annotate(
            month=TruncMonth('order_date')
        )
        .values('month')
        .annotate(
            total=Sum('total_amount')
        )
        .order_by('month')
    )

    for item in monthly_sales:

        if item['month']:

            key = item['month'].strftime('%Y-%m')

            monthly_orders[key] = {
                'label': item['month'].strftime('%b %Y'),
                'sales': float(item['total'] or 0),
                'payments': 0,
                'expenses': 0,
            }

    monthly_payments = (
        payment_queryset
        .annotate(
            month=TruncMonth('payment_date')
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )

    for item in monthly_payments:

        if item['month']:

            key = item['month'].strftime('%Y-%m')

            if key not in monthly_orders:

                monthly_orders[key] = {
                    'label': item['month'].strftime('%b %Y'),
                    'sales': 0,
                    'payments': 0,
                    'expenses': 0,
                }

            monthly_orders[key]['payments'] = float(
                item['total'] or 0
            )

    monthly_expenses = (
        expense_queryset
        .annotate(
            month=TruncMonth('expense_date')
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )

    for item in monthly_expenses:

        if item['month']:

            key = item['month'].strftime('%Y-%m')

            if key not in monthly_orders:

                monthly_orders[key] = {
                    'label': item['month'].strftime('%b %Y'),
                    'sales': 0,
                    'payments': 0,
                    'expenses': 0,
                }

            monthly_orders[key]['expenses'] = float(
                item['total'] or 0
            )

    monthly_business = []

    for key in sorted(monthly_orders.keys()):

        sales = monthly_orders[key]['sales']
        payments = monthly_orders[key]['payments']
        expenses = monthly_orders[key]['expenses']

        monthly_business.append(
            {
                'label': monthly_orders[key]['label'],
                'sales': sales,
                'payments': payments,
                'expenses': expenses,
                'net': sales - expenses,
            }
        )

    # =========================
    # PDF RESPONSE
    # =========================

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="smart_boutique_business_report.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    # =========================
    # COLORS
    # =========================

    dark_brown = colors.HexColor('#5b3a29')
    dark_text = colors.HexColor('#211c19')
    light_bg = colors.HexColor('#f7f3f0')
    gold = colors.HexColor('#e7c98a')
    grey = colors.HexColor('#777777')
    white = colors.white
    border = colors.HexColor('#dddddd')

    # =========================
    # PAGE HEADER
    # =========================

    def draw_header():

        pdf.setFillColor(dark_brown)

        pdf.rect(
            0,
            height - 88,
            width,
            88,
            fill=1,
            stroke=0
        )

        pdf.setFillColor(white)

        pdf.setFont(
            "Helvetica-Bold",
            21
        )

        pdf.drawString(
            45,
            height - 38,
            "Smart Boutique"
        )

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            45,
            height - 56,
            "Smart Tailoring & Boutique"
        )

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.drawRightString(
            width - 45,
            height - 45,
            "BUSINESS REPORT"
        )

    # =========================
    # FOOTER
    # =========================

    page_number = [1]

    def draw_footer():

        pdf.setStrokeColor(border)

        pdf.line(
            45,
            42,
            width - 45,
            42
        )

        pdf.setFillColor(grey)

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.drawString(
            45,
            27,
            "Smart Boutique - Business Report"
        )

        pdf.drawCentredString(
            width / 2,
            27,
            f"Page {page_number[0]}"
        )

        pdf.drawRightString(
            width - 45,
            27,
            "Generated from Smart Boutique"
        )

    # =========================
    # NEW PAGE
    # =========================

    def new_page():

        pdf.showPage()

        page_number[0] += 1

        draw_header()
        draw_footer()

    # =====================================================
    # PAGE 1
    # =====================================================

    draw_header()
    draw_footer()

    y = height - 120

    # REPORT TITLE

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        19
    )

    pdf.drawString(
        45,
        y,
        "Business Report"
    )

    y -= 24

    pdf.setFillColor(grey)

    pdf.setFont(
        "Helvetica",
        9
    )

    if from_date or to_date:

        date_text = (
            f"Report Period: "
            f"{from_date or 'All'} to "
            f"{to_date or 'All'}"
        )

    else:

        date_text = "Report Period: All Dates"

    pdf.drawString(
        45,
        y,
        date_text
    )

    # =====================================================
    # BUSINESS SUMMARY
    # =====================================================

    y -= 42

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        45,
        y,
        "Business Summary"
    )

    y -= 18

    box_y = y - 72

    pdf.setFillColor(light_bg)

    pdf.roundRect(
        45,
        box_y,
        width - 90,
        72,
        8,
        fill=1,
        stroke=0
    )

    pdf.setStrokeColor(border)

    pdf.roundRect(
        45,
        box_y,
        width - 90,
        72,
        8,
        fill=0,
        stroke=1
    )

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        62,
        box_y + 43,
        str(customer_count)
    )

    pdf.drawString(
        188,
        box_y + 43,
        str(product_count)
    )

    pdf.drawString(
        315,
        box_y + 43,
        str(order_count)
    )

    pdf.drawString(
        440,
        box_y + 43,
        str(inventory_count)
    )

    pdf.setFillColor(grey)

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawString(
        62,
        box_y + 25,
        "Customers"
    )

    pdf.drawString(
        188,
        box_y + 25,
        "Products"
    )

    pdf.drawString(
        315,
        box_y + 25,
        "Orders"
    )

    pdf.drawString(
        440,
        box_y + 25,
        "Inventory"
    )

    y = box_y - 40

    # =====================================================
    # FINANCIAL SUMMARY
    # =====================================================

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        45,
        y,
        "Financial Summary"
    )

    y -= 22

    # SALES

    pdf.setFillColor(light_bg)

    pdf.roundRect(
        45,
        y - 25,
        width - 90,
        32,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        58,
        y - 13,
        "Total Sales"
    )

    pdf.drawRightString(
        width - 58,
        y - 13,
        f"Rs. {float(total_sales):,.2f}"
    )

    y -= 42

    # PAYMENTS

    pdf.setFillColor(light_bg)

    pdf.roundRect(
        45,
        y - 25,
        width - 90,
        32,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark_text)

    pdf.drawString(
        58,
        y - 13,
        "Total Payments"
    )

    pdf.drawRightString(
        width - 58,
        y - 13,
        f"Rs. {float(total_payments):,.2f}"
    )

    y -= 42

    # EXPENSES

    pdf.setFillColor(light_bg)

    pdf.roundRect(
        45,
        y - 25,
        width - 90,
        32,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark_text)

    pdf.drawString(
        58,
        y - 13,
        "Total Expenses"
    )

    pdf.drawRightString(
        width - 58,
        y - 13,
        f"Rs. {float(total_expenses):,.2f}"
    )

    y -= 42

    # PENDING BALANCE

    pdf.setFillColor(
        colors.HexColor('#fff4df')
    )

    pdf.roundRect(
        45,
        y - 28,
        width - 90,
        35,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        dark_text
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        58,
        y - 14,
        "Pending Balance"
    )

    pdf.drawRightString(
        width - 58,
        y - 14,
        f"Rs. {float(pending_balance):,.2f}"
    )

    # IMPORTANT GAP BETWEEN PENDING AND NET

    y -= 58

    # NET BALANCE

    pdf.setFillColor(gold)

    pdf.roundRect(
        45,
        y - 40,
        width - 90,
        47,
        8,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        58,
        y - 14,
        "Net Balance"
    )

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawRightString(
        width - 58,
        y - 14,
        f"Rs. {float(net_balance):,.2f}"
    )

    # =====================================================
    # ORDER STATUS
    # =====================================================

    y -= 78

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        45,
        y,
        "Order Status Summary"
    )

    y -= 23

    status_data = [
        ("Pending", pending_orders),
        ("Processing", processing_orders),
        ("Completed", completed_orders),
        ("Cancelled", cancelled_orders),
    ]

    left_x = 55
    right_x = width / 2 + 20

    for index, (label, count) in enumerate(status_data):

        if index % 2 == 0:

            x = left_x

        else:

            x = right_x

        row_y = y - (index // 2) * 25

        pdf.setFillColor(light_bg)

        pdf.roundRect(
            x,
            row_y - 15,
            220,
            23,
            5,
            fill=1,
            stroke=0
        )

        pdf.setFillColor(dark_text)

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            x + 10,
            row_y - 7,
            label
        )

        pdf.setFont(
            "Helvetica-Bold",
            9
        )

        pdf.drawRightString(
            x + 210,
            row_y - 7,
            str(count)
        )

    # =====================================================
    # PAGE 2 - MONTHLY REPORT
    # =====================================================

    new_page()

    y = height - 120

    pdf.setFillColor(dark_text)

    pdf.setFont(
        "Helvetica-Bold",
        17
    )

    pdf.drawString(
        45,
        y,
        "Monthly Business Report"
    )

    y -= 30

    table_x = 45
    table_width = width - 90

    col_widths = [
        75,
        100,
        100,
        100,
        table_width - 375
    ]

    row_height = 26

    headers = [
        "Month",
        "Sales",
        "Payments",
        "Expenses",
        "Net Balance",
    ]

    # TABLE HEADER

    pdf.setFillColor(dark_brown)

    pdf.roundRect(
        table_x,
        y - row_height,
        table_width,
        row_height,
        5,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(white)

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    x = table_x

    for index, header in enumerate(headers):

        pdf.drawString(
            x + 7,
            y - 17,
            header
        )

        x += col_widths[index]

    y -= row_height

    # TABLE DATA

    if monthly_business:

        for row in monthly_business:

            if y < 75:

                new_page()

                y = height - 120

                pdf.setFillColor(dark_text)

                pdf.setFont(
                    "Helvetica-Bold",
                    15
                )

                pdf.drawString(
                    45,
                    y,
                    "Monthly Business Report - Continued"
                )

                y -= 28

                pdf.setFillColor(dark_brown)

                pdf.roundRect(
                    table_x,
                    y - row_height,
                    table_width,
                    row_height,
                    5,
                    fill=1,
                    stroke=0
                )

                pdf.setFillColor(white)

                pdf.setFont(
                    "Helvetica-Bold",
                    8
                )

                x = table_x

                for index, header in enumerate(headers):

                    pdf.drawString(
                        x + 7,
                        y - 17,
                        header
                    )

                    x += col_widths[index]

                y -= row_height

            pdf.setFillColor(light_bg)

            pdf.rect(
                table_x,
                y - row_height,
                table_width,
                row_height,
                fill=1,
                stroke=0
            )

            pdf.setFillColor(dark_text)

            values = [
                row['label'],
                f"Rs. {row['sales']:,.2f}",
                f"Rs. {row['payments']:,.2f}",
                f"Rs. {row['expenses']:,.2f}",
                f"Rs. {row['net']:,.2f}",
            ]

            x = table_x

            for index, value in enumerate(values):

                if index == 4:

                    pdf.setFont(
                        "Helvetica-Bold",
                        8
                    )

                else:

                    pdf.setFont(
                        "Helvetica",
                        8
                    )

                pdf.drawString(
                    x + 7,
                    y - 17,
                    value
                )

                x += col_widths[index]

            y -= row_height

    else:

        pdf.setFillColor(grey)

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            55,
            y - 20,
            "No monthly business data available."
        )

    # =====================================================
    # OVERALL NET BALANCE
    # =====================================================

    if y > 95:

        y -= 30

        pdf.setFillColor(gold)

        pdf.roundRect(
            table_x,
            y - 40,
            table_width,
            45,
            8,
            fill=1,
            stroke=0
        )

        pdf.setFillColor(dark_text)

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            table_x + 12,
            y - 19,
            "Overall Net Balance"
        )

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawRightString(
            width - 58,
            y - 19,
            f"Rs. {float(net_balance):,.2f}"
        )

    # =====================================================
    # SAVE
    # =====================================================

    pdf.save()

    return response

