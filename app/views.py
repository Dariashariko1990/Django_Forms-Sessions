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
    is_review_exist = False

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Review.objects.create(text=cleaned_data['text'], product=product)
            is_review_exist = True
            # попытка добавлять id продукта в request.session, чтобы затем проверять наличие отзыва
            # от этого пользователя
            if not request.session['reviewed_products']:
                request.session['reviewed_products'] = [product.id]
            else:
                request.session['reviewed_products'].append(product.id)
            # не сработала логика, перемещаясь со страницы одного продукта на страницу другого
            # обнуляется request.session['reviewed_products']

    context = {
        'form': ReviewForm,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist,
    }

    return render(request, template, context)
