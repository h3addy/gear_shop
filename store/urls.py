from store.views import AllProductView, CartView, CheckoutView, LandingPageView, NewArrivalsView, PopularItemsView, ProcessOrder, SignupView, UpdateItem
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

app_name = 'store'
urlpatterns = [
    # store navigation urls
    path('products/',AllProductView.as_view(), name='all_products_page'),
    path('popular_items/',PopularItemsView.as_view(), name='popular_items_page'),
    path('new_arrivals/',NewArrivalsView.as_view(), name='new_arrivals_page'),
    path('cart/',CartView.as_view(), name='cart_page'),
    path('checkout/',CheckoutView.as_view(), name='checkout_page'),
    path('update_item/', UpdateItem.as_view(), name='update_item'),
    path('process_order/', ProcessOrder.as_view(), name='process_order'),
]
