from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import InventoryItem
from .forms import InventoryForm
from products.models import Product


@login_required(login_url='/login/')
def inventory_list(request):
    search = request.GET.get('search', '')

    items = InventoryItem.objects.all()

    if search:
        items = items.filter(
            name__icontains=search
        ) | items.filter(
            category__icontains=search
        )

    items = items.order_by('id')

    inventory_data = []

    for item in items:
        product = Product.objects.filter(
            name=item.name
        ).first()

        inventory_data.append({
            'item': item,
            'product': product,
        })

    return render(
        request,
        'inventory/inventory_list.html',
        {
            'inventory_data': inventory_data,
            'search': search
        }
    )


@login_required(login_url='/login/')
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)

        if form.is_valid():
            item = form.save()

            # Find matching Product
            product = Product.objects.filter(
                name=item.name
            ).first()

            if product:
                # Inventory -> Product Sync
                product.name = item.name
                product.category = item.category
                product.price = item.price
                product.stock = item.quantity
                product.description = item.description
                product.save()
            else:
                # If Product does not exist, create it automatically.
                Product.objects.create(
                    name=item.name,
                    category=item.category,
                    price=item.price,
                    stock=item.quantity,
                    description=item.description
                )

            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(
        request,
        'inventory/add_inventory.html',
        {
            'form': form
        }
    )


@login_required(login_url='/login/')
def edit_inventory(request, id):
    item = get_object_or_404(
        InventoryItem,
        id=id
    )

    old_name = item.name

    if request.method == 'POST':
        form = InventoryForm(
            request.POST,
            instance=item
        )

        if form.is_valid():
            item = form.save()

            # Find Product using OLD name
            product = Product.objects.filter(
                name=old_name
            ).first()

            if product:
                # Inventory -> Product Sync
                product.name = item.name
                product.category = item.category
                product.price = item.price
                product.stock = item.quantity
                product.description = item.description
                product.save()
            else:
                # Safety: create Product if missing
                Product.objects.create(
                    name=item.name,
                    category=item.category,
                    price=item.price,
                    stock=item.quantity,
                    description=item.description
                )

            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)

    return render(
        request,
        'inventory/edit_inventory.html',
        {
            'form': form,
            'item': item
        }
    )


@login_required(login_url='/login/')
def delete_inventory(request, id):
    item = get_object_or_404(
        InventoryItem,
        id=id
    )

    if request.method == 'POST':
        # Find matching Product
        product = Product.objects.filter(
            name=item.name
        ).first()

        # Delete Product
        if product:
            product.delete()

        # Delete Inventory
        item.delete()

        return redirect('inventory_list')

    return render(
        request,
        'inventory/delete_inventory.html',
        {
            'item': item
        }
    )


@login_required(login_url='/login/')
def view_inventory(request, id):
    item = get_object_or_404(
        InventoryItem,
        id=id
    )

    product = Product.objects.filter(
        name=item.name
    ).first()

    return render(
        request,
        'inventory/view_inventory.html',
        {
            'item': item,
            'product': product
        }
    )
