from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import uuid




class Register(models.Model):
    name = models.CharField(max_length=255),
    password = models.CharField(max_length= 20),
    email = models.CharField(max_length=255)

class regExtra(models.Model):
    phoneno = models.CharField(max_length=255),
    address = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
                return self.name 

class ProdCat(models.Model):
    product_id=models.AutoField
    image = models.ImageField(upload_to="images/", null=True)
    name = models.CharField(max_length=50, null=True)
    desc = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    slug =  AutoSlugField(populate_from='name', null=True)



class Customer(models.Model):
     user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)
     name = models.CharField(max_length=200,null=True),
     email = models.CharField(max_length=200, null=True)

     def __str__(self):
          return self.name
     
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])   #calculating final total for all orderitems
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(ProdCat, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.our_price * self.quantity  #calculating total price for each item based on the quantity
		return total

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    activity_details = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

ORDER_STATUS = (
    ('Ordered','ORDERED'),
    ('Shipped', 'SHIPPED'),
    ('Delivered','DELIVERED'),
)

DELIVERY_STATUS = (
    ('Successful','Successful'),
    ('Unsuccessful', 'Unsuccessful'),  
)


class Track(models.Model):
      username = models.CharField(max_length=255,default="")
      orderTitle = models.CharField(max_length=255,default="")
      orderDesc = models.CharField(max_length=255, default="")
      orderPrice = models.CharField(max_length=255, default="")
      image = models.ImageField(upload_to="images/", null=True)
      status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Ordered')
      deliverystatus = models.CharField(max_length=50,choices=DELIVERY_STATUS, default="Successful")



""" class Payment(models.Model):
        sno = models.AutoField(primary_key=True)
        name = models.CharField(max_length=255)
        phone = models.CharField(max_length=12)
        address = models.CharField(max_length=255)
        mode = models.CharField(max_length=255)
        size = models.IntegerField(default=32, null=True)
        payment_status = models.BooleanField(default=False)
        delivered = models.BooleanField(default=False)

        def __str__(self):
                return 'Product brought by ' +self.name  """

    
  