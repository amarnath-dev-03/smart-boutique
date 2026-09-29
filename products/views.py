from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm

from inventory.models import InventoryItem


def product_list(request):

    search = request.GET.get('search', '')

    products = Product.objects.all()

    if search:
        products = products.filter(
            name__icontains=search
        ) | products.filter(
            category__icontains=search
        )

    return render(request, 'products/product_list.html', {
        'products': products,
        'search': search
    })


def add_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST)

        if form.is_valid():

            product = form.save()

            # Automatically create stock item
            InventoryItem.objects.create(
                name=product.name,
                category=product.category,
                quantity=product.stock,
                price=product.price,
                description=product.description
            )

            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {
        'form': form
    })


def view_product(request, id):

    product = get_object_or_404(Product, id=id)

    return render(request, 'products/view_product.html', {
        'product': product
    })


def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    old_name = product.name

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            # Update matching inventory item
            inventory_item = InventoryItem.objects.filter(
                name=old_name
            ).first()

            if inventory_item:

                inventory_item.name = product.name
                inventory_item.category = product.category
                inventory_item.quantity = product.stock
                inventory_item.price = product.price
                inventory_item.description = product.description

                inventory_item.save()

            else:

                # If inventory item does not exist, create it
                InventoryItem.objects.create(
                    name=product.name,
                    category=product.category,
                    quantity=product.stock,
                    price=product.price,
                    description=product.description
                )

            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    return render(request, 'products/add_product.html', {
        'form': form
    })


def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':

        # Delete matching inventory item
        InventoryItem.objects.filter(
            name=product.name
        ).delete()

        product.delete()

        return redirect('product_list')

    return render(request, 'products/delete_product.html', {
        'product': product
    })
