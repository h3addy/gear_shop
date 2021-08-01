from django.db import models
from django.db.models.signals import post_save


# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=200, null=True, blank=True)
    # email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.email

class ProductCategory(models.Model):
    category = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.category)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    current_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    popular = models.BooleanField(default=False, null=True, blank=True)
    new_arrival = models.BooleanField(default=False, null=True, blank=True)
    discount_offer = models.BooleanField(default=False, null=True, blank=True)
    old_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        return '/images/no-image.jpg'
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
                break
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        quantity = sum([item.quantity for item in orderitems])
        return quantity

    def __str__(self):
        return self.customer.user.email

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.current_price
        return total

    def __str__(self):
        return self.order.customer.user.email

class ShippigAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=DO_NOTHING, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.address


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)

