from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView)
from .models import Category , Product
from django.shortcuts import get_object_or_404


class ProductList(ListView):
    model = Product
    template_name = "shop/product/list.html"
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug) 
            queryset = queryset.filter(category=category)
        return queryset 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['categories'] = Category.objects.all()
        context['category'] = get_object_or_404(Category, slug=category_slug) if category_slug else None
        return context
    

def product_detail(request, id, slug):
    product = get_object_or_404(Product, 
                                id=id, 
                                slug=slug, 
                                available=True)
    
    return render(
        request, 'shop/product/detail.html', {'product':product}
    )