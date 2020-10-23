from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True,default='')
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    Transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property
    def get_comment(self):
        return self.comments.filter(parent__isnull=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        return self.quantity*self.product.price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200,null=False)
    zipcode =  models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=800,null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    parent = models.ForeignKey('self',verbose_name="thisParent",on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment '+ str(self.id) + ' for '+self.product.name

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username)


@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.name=instance.username
        instance.customer.save()
