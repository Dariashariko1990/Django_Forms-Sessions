from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product.id)
    reviewed_products = request.session.get('reviewed_products', '[]')
    if product.id in reviewed_products:
        is_review_exist = True
    else:
        is_review_exist = False

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Review.objects.create(text=cleaned_data['text'], product=product)
            is_review_exist = True
            if len(reviewed_products) == 0:
                reviewed_products.append(product.id)
                request.session['reviewed_products'] = reviewed_products
            else:
                reviewed_products.append(product.id)
                request.session['reviewed_products'] = reviewed_products

    context = {
        'form': ReviewForm,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist,
    }

    return render(request, template, context)
