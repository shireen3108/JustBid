from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    street_address = models.CharField(max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=30, blank=True, null=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True, default='')
    zipcode = models.CharField('Zip Code', max_length=5, blank=True, null=True, default='')
    mobile_num = models.CharField('Mobile Number', max_length=15, blank=True, null=True)
    email = models.EmailField(null=False, unique=True, error_messages={'unique': 'A user with that email already exists.'})
    # first_name = models.CharField(max_length=30, blank=False)
    # last_name = models.CharField(max_length=150, blank=False)
    class Meta:
        verbose_name = "Customer"

class Item(models.Model):
    name=models.CharField(max_length=50, blank=False)
    price=models.DecimalField(max_digits=5,blank=False, decimal_places=2)
    start_date= models.DateTimeField()
    end_date= models.DateTimeField()
    image=models.ImageField(upload_to="items/images", null=True)
    comments= models.CharField(max_length=300, null=True, blank=True)
    customer_id= models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='item_customer_id')

    class Meta:
        verbose_name = "Item"

    def __str__(self):
        return self.name


class Bid(models.Model):
    amount= models.DecimalField(max_digits=5,blank=False, decimal_places=2)
    time= models.DateTimeField()
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bid_item_id')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bid_customer_id')

    class Bid:
        verbose_name = "Bid"

    def __str__(self):
        return self.item_id.name + ' for ' + str(self.amount) + ' by ' + self.customer_id.first_name

