from django.views.generic.base import View
from store.models import Customer, Order, OrderItem, Product, ShippigAddress
from typing import Generic
from django.shortcuts import render, resolve_url, reverse
from django.views import generic
from .forms import CustomUserCreationForm
from django.http import JsonResponse, request
import json
import datetime
from .utils import get_items_order_cartItems, geustOrder

# Create your views here.
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cartItems': (get_items_order_cartItems(self.request))['cartItems']
        })
        return context

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse("sign_in_page") 

class AllProductView(generic.ListView):
    template_name = 'store/products.html'
    context_object_name = 'products'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cartItems': (get_items_order_cartItems(self.request))['cartItems']
        })
        return context

class PopularItemsView(generic.TemplateView):
    template_name = 'store/products.html'
    queryset = Product.objects.filter(popular=True)
    # print(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
        else:
            cartItems = 0
        context.update({
            'products': self.queryset,
            'cartItems': (get_items_order_cartItems(self.request))['cartItems']
        })
        return context

class NewArrivalsView(generic.TemplateView):
    template_name = 'store/products.html'
    queryset = Product.objects.filter(new_arrival=True)
    # print(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
        else:
            cartItems = 0
        context.update({
            'products': self.queryset,
            'cartItems': (get_items_order_cartItems(self.request))['cartItems']
        })
        return context

class CartView(generic.TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_items_order_cartItems(self.request))
        return context

class CheckoutView(generic.TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_items_order_cartItems(self.request))
        return context

class UpdateItem(View):
    def post(self, request):
        if request:
            data = json.loads(request.body)
            productID = data['productID']
            action = data['action']

            customer = request.user.customer
            product = Product.objects.get(id=productID)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
            if action == 'add':
                orderitem.quantity = orderitem.quantity + 1
            elif action == 'remove':
                orderitem.quantity = orderitem.quantity - 1
            orderitem.save()

            if orderitem.quantity <= 0:
                orderitem.delete()

            return JsonResponse("Item", safe=False)

class ProcessOrder(View):
    def post(self, request):
        if request:
            data = json.loads(request.body)
            transaction_id = datetime.datetime.now().timestamp()

            if self.request.user.is_authenticated:
                customer = self.request.user.customer
                order, created = Order.objects.get_or_create(customer=customer, complete=False)    
            else:
                customer, order = geustOrder(self.request, data)

        total =  float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippigAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )

        return JsonResponse("Item", safe=False)