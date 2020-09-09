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

    form = ReviewForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.product = Product.objects.get(pk=pk)
            review.save()

            request.session['reviewed_products'] = [pk] if not request.session.get('reviewed_products') else request.session['reviewed_products'].append(pk)

    context = {
        'form': form,
        'product': product
    }

    return render(request, template, context)
