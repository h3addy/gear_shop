from .models import *
import json

def get_items_order_cartItems(request):
    """
    This method returns items, orders and orditems in a dictionary.
    """
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart'))
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'cartItems': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.current_price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id': product.id,
                        'name': product.name,
                        'current_price': product.current_price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    
    context.update({
        'items': items,
        'order': order,
        'cartItems': cartItems,
    })
    return context

def geustOrder(request, data):
    print(request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = get_items_order_cartItems(request)
    items = cookieData['items']

    user, created = User.objects.get_or_create(email=email, username=name)
    user.save()
    customer = Customer.objects.get(user=user)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])
    
    return customer, order
        