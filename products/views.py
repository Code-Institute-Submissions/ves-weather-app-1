from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from cart.models import Cart

from .models import Product

class ProductFeaturedListView(ListView):
    template_name = "products/products.html"
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()
        
class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-details.html"
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/products.html"
    
    
class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product-details.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Error!")
            
        return instance

class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/product-details.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product does not exist.")
        return instance