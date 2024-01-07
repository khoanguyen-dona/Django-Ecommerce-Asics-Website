from django.db import models
from django.contrib.auth.models import User

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
        return self.title+ '___#'+ str(self.id)

class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    thumbnail=models.ImageField(upload_to='products/thumbnails')
    marked_price=models.BigIntegerField()
    selling_price=models.BigIntegerField()
    description=models.TextField(blank=True)  
    view_count=models.BigIntegerField(default=0)
    sex=models.BooleanField(blank=True,default=False)
    

    def __str__(self):
        return self.title + '___#'+ str(self.id)
    
class ProductSize(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    size_6=models.BooleanField(blank=True)
    size_6h=models.BooleanField(blank=True)
    size_7=models.BooleanField(blank=True)
    size_7h=models.BooleanField(blank=True)
    size_8=models.BooleanField(blank=True)
    size_8h=models.BooleanField(blank=True)
    size_9=models.BooleanField(blank=True)
    size_9h=models.BooleanField(blank=True)
    size_10=models.BooleanField(blank=True)
    size_10h=models.BooleanField(blank=True)
    size_11=models.BooleanField(blank=True)
    size_S=models.BooleanField(blank=True,default=False)
    size_M=models.BooleanField(blank=True,default=False)   
    size_L=models.BooleanField(blank=True,default=False)   
    size_XL=models.BooleanField(blank=True,default=False)   
    size_XXL=models.BooleanField(blank=True,default=False)   

    
    def __str__(self):
        return self.product.title

class WishList(models.Model):
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,null=True,blank=True)
    count=models.IntegerField(null=True,blank=True)

    def __str__(self):      
        return 'wishlist :'+str(self.id)    
        
class WishListItem(models.Model):
    wishlist=models.ForeignKey(WishList,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return  'wish list : '+str(self.wishlist.id) + 'wish_list_item :'+str(self.id)
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/images/')

    def __str__(self):
        return self.product.title
    
class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    total=models.BigIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return 'cart :'+str(self.id)
        # return str(self.id)
    
class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.BigIntegerField()
    quantity=models.BigIntegerField()
    subtotal=models.BigIntegerField()
    size=models.CharField(null=True,blank=True,max_length=10)
    sex=models.CharField(max_length=10,blank=True,null=True)


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
    # subtotal=models.BigIntegerField()
    discount=models.BigIntegerField()
    total=models.BigIntegerField()
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order : ' +str(self.id)
