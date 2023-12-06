from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
# Create your models here.

class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='admins_avatar')
    mobile=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username



class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200,null=True,blank=True)
    joined_on=models.DateTimeField(auto_now_add=True)
    avatar=models.ImageField(upload_to='customer_avatar',blank=True,null=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    thumbnail=models.ImageField(upload_to='products/thumbnails')
    marked_price=models.BigIntegerField()
    selling_price=models.BigIntegerField()
    description=models.TextField()  
    warranty=models.CharField(max_length=300,null=True,blank=True)
    return_policy=models.CharField(max_length=300,null=True,blank=True)
    view_count=models.BigIntegerField(default=0)

    def __str__(self):
        return self.title + '___#'+ str(self.id)
        

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/images/')

    def __str__(self):
        return self.product.title
    
class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    total=models.BigIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'cart :'+str(self.id)
        # return str(self.id)
    
class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.BigIntegerField()
    quantity=models.BigIntegerField()
    subtotal=models.BigIntegerField()

    def __str__(self):
        return 'Cart: '+str(self.cart.id) + 'CartProduct: '+str(self.id)
    
ORDER_STATUS=(
    ('Order received','Order received'),
    ('Order processing','Order processing'),        
    ('On delivery','On delivery'),
    ('Order completed','Order completed'),
    ('Order canceled','Order canceled'),

)
    
class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    ordered_by=models.CharField(max_length=200)
    shipping_address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=12)
    email=models.EmailField(null=True,blank=True)
    subtotal=models.BigIntegerField()
    discount=models.BigIntegerField()
    total=models.BigIntegerField()
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order : ' +str(self.id)
