from django.views.generic import TemplateView,CreateView,FormView,ListView,View,DetailView
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings



class HomeView(TemplateView):
    template_name='home.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        wishlist=WishList.objects.all()
        all_products=Product.objects.all().order_by('-id')
        paginator=Paginator(all_products,12)
        page_number=self.request.GET.get('page')
        product_list=paginator.get_page(page_number)
        context['wishlist']=wishlist
        context['product_list']=product_list
        return context

class AllProductsView(TemplateView):
    template_name='allproducts.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['allcategories']=Category.objects.all()
        return context

# class ProductDetailView(TemplateView):
#     template_name='productdetail.html'

#     def get_context_data(self,**kwargs):
#         context=super().get_context_data(**kwargs)
#         url_slug=self.kwargs['slug']
#         context['product']=Product.objects.get(slug=url_slug)

#         return context
def ProductDetailView(request,slug):
    product = Product.objects.get(slug=slug)
    product.view_count+=1
    product.save()
    return render(request, 'productdetail.html', {'product': product})

class AddToCartView(TemplateView):
    
    def get(self,request,*args,**kwargs):
        pre_url = request.META.get('HTTP_REFERER')
        product_id=self.kwargs['pro_id']
        # product in database
        product_obj=Product.objects.get(id=product_id)
        # cart id session
        cart_id=self.request.session.get("cart_id", None)
        # if cart already exist 
        if Cart.objects.filter(id=cart_id).exists():
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            # sản phẩm có trong cart thì không tạo mới,thực hiện logic + thêm
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.selling_price
                cartproduct.save()
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
            # sản phẩm chưa từng xuất hiện trong cart ta tạo mới
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,
                        rate=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
        # create new cart if deos no  exits
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,
                                                   quantity=1,subtotal=product_obj.selling_price)
            cart_obj.total+=product_obj.selling_price
            if self.request.user.is_authenticated:
                cart_obj.customer=self.request.user.customer

            cart_obj.save()
        messages.success(request, 'Sản phẩm đã được thêm vào giỏ hàng !')

        return redirect(pre_url)

class ManageCartView(TemplateView):
    def get(self,request,*args,**kwargs):
        pre_url = request.META.get('HTTP_REFERER')
        cp_id=self.kwargs['cp_id']
        action=request.GET.get('action')
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart

        if action=='inc':
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
        elif action=='dcr':
            cp_obj.quantity-=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-=cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity<=0:
                cp_obj.delete()
        elif action=='rmv':
            cart_obj.total-=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect(pre_url)

class EmptyCartView(TemplateView):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect('ecomapp:mycart')

class MyCartView(TemplateView):
    template_name='mycart.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart
        return context
    
class WishListView(TemplateView):
    template_name='wishlist.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        wishlist_id=self.request.session.get('wishlist_id',None)
        if wishlist_id:
            wishlist=WishList.objects.get(id=wishlist_id)
        else:
            wishlist=None
        context['wishlist']=wishlist
        return context



class AddToWishListView(TemplateView):
    def get(self,request,*args,**kwargs):
        pre_url = request.META.get('HTTP_REFERER')
        product_id=self.kwargs['pro_id']
        # product in database
        product_obj=Product.objects.get(id=product_id)
        # wishlist_id session
        wishlist_id=self.request.session.get("wishlist_id", None)
        # nếu wishlist_session đã tồn tại thì dùng nó
        if WishList.objects.filter(id=wishlist_id).exists():
            wishlist_obj=WishList.objects.get(id=wishlist_id)

            item_in_wishlist=wishlist_obj.wishlistitem_set.filter(product=product_obj)
            # sản phẩm có trong cart thì không tạo mới,thực hiện logic + thêm
            if item_in_wishlist.exists():
                wishlist_item=item_in_wishlist.last()
                wishlist_item.save()
                wishlist_obj.save()
            # sản phẩm chưa từng xuất hiện trong cart ta tạo mới
            else:
                wishlist_item=WishListItem.objects.create(wishlist=wishlist_obj,product=product_obj)
                wishlist_obj.save()

        # if wishlist_session chưa có thì tạo mới
        else:
            wishlist_obj=WishList.objects.create()
            self.request.session['wishlist_id']=wishlist_obj.id

            if self.request.user.is_authenticated:
                wishlist_obj.customer=self.request.user.customer

            wishlist_obj.save()
        messages.success(request, 'Sản phẩm đã được thêm vào yêu thích !')

        return redirect(pre_url)

class RemoveFromWishListView(TemplateView):
    def get(self,request,*args,**kwargs):
        pre_url = request.META.get('HTTP_REFERER')
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)
        wishlistitem_obj=WishListItem.objects.get(product=product_obj)
        wishlistitem_obj.delete()

        return redirect(pre_url)
class CheckoutView(CreateView):
    template_name='checkout.html'
    form_class=CheckoutForm
    success_url=reverse_lazy('ecomapp:home')
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context
    def form_valid(self, form):
        cart_id=self.request.session.get('cart_id')
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status="Order received"
            del self.request.session['cart_id']
            messages.success(self.request,'Đặt hàng thành công!')

            # cart_product_obj=CartProduct.objects.get(cart=cart_obj)
            # price=cart_product_obj.product.selling_price
            # quantity=cart_product_obj.quantity

            # email=self.request.user.email
            # text_content='Thông báo xác nhận đơn hàng '
            # html_content='''
            # <html>
            # <body>    
            
            # <p> ASICS VIETNAM đã nhận được thông tin đặt hàng của bạn +{{cart_product_obj.product.title}} </p>
            # <p> Giá: {{cart_product_obj.product.price}}</p>
            
            # </body>
            # </html>
            # '''
            # send_mail(
            #     'Asics Viet Nam',
            #     text_content+html_content,
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )
        else:
            return redirect('ecomapp:home')
        return super().form_valid(form)

class CustomerRegistrationView(CreateView):
    template_name='customerRegistration.html'
    form_class=CustomerRegistrationForm
    success_url=reverse_lazy('ecomapp:customerlogin')

    def form_valid(self,form):
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        email=form.cleaned_data.get('email')
        user=User.objects.create_user(username,email,password)
        form.instance.user=user
        messages.success(self.request,'Đăng kí thành công!')
        
        return super().form_valid(form)

class CustomerLogoutView(TemplateView):
    def get(self,request):
        logout(request)
        messages.success(request,'Đăng xuất thành công!')
        return redirect('ecomapp:home')
    
class CustomerLoginView(FormView):
    template_name='customerLogin.html'
    form_class=CustomerLoginForm
    success_url=reverse_lazy('ecomapp:home')    

    def form_valid(self,form):
        uname=form.cleaned_data.get('username')
        pword=form.cleaned_data.get('password')
        usr=authenticate(username=uname,password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
            messages.success(self.request,'Đăng nhập thành công!')
            cart_id=self.request.session.get('cart_id',None)
            if cart_id:
                self.request.session['cart_id']
                cart_obj=Cart.objects.get(id=cart_id)
                cart_obj.customer=self.request.user.customer    
                cart_obj.save()      
            else :
                pass
        else: 
            return render(self.request,self.template_name,{'form':self.form_class,'error1':'Không hợp lệ'})
        return super().form_valid(form)
   
class PasswordForgotView(FormView):
    template_name='forgotpassword.html'
    form_class=PasswordForgotForm
    success_url='/forgot-password/?m=s'

    def form_valid(self,form):
        # lấy email từ user
        email=form.cleaned_data.get('email')
        # địa chỉ host ip/domain hiện tại
        current_url=self.request.META['HTTP_HOST']
        # user có tồn tại email khi nhập
        customer=Customer.objects.get(user__email=email)
        user=customer.user
        # gửi mail tới user bằng gmail
        text_content='Click vào link dưới đây để reset password. '
        html_content= current_url + '/password-reset/' +email +'/'+ password_reset_token.make_token(user) +'/'
        send_mail(
            'Reset Password | Asics Viet Nam',
            text_content+html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return super().form_valid(form)
    
class PasswordResetView(FormView):
    template_name='passwordreset.html'
    form_class=PasswordResetForm
    success_url='/login/'

    def dispatch(self,request,*args,**kwargs):
        email=self.kwargs.get('email')
        user=User.objects.get(email=email)
        token=self.kwargs.get('token')
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else: 
            return redirect(reverse_lazy('ecomapp:passwordforgot')+ '?m=e')

        return super().dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        password=form.cleaned_data['new_password']
        email=self.kwargs.get('email')
        user=User.objects.get(email=email)
        user.set_password(password)
        user.save()
        messages.success(self.request,'Reset mật khẩu thành công!')
        return super().form_valid(form)



class AboutView(TemplateView):
    template_name='about.html' 

class ContactView(TemplateView):
    template_name='contactus.html'

# customer------------------
# phai co tai khoan moi xem profile duoc,ngăn chặn việc customer quay trở lại sau bằng nút go back sau khi logout vẫn xem thông tin cũ được
# customer không thể nhấn nút go back để xem thông tin trong profile cũ,phải đăng nhập lại trang login mới xem dược
class CustomerRequiredMixin(object):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('ecomapp:customerlogin')
        return super().dispatch(request,*args,**kwargs)

class CustomerProfileView(CustomerRequiredMixin,TemplateView):
    template_name='customerprofile.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        orders=Order.objects.filter(cart__customer=customer).order_by('-id')
        context['customer']=customer
        context['orders']=orders
        return context
    
    
class CustomerOrderDetailView(CustomerRequiredMixin,TemplateView):
    template_name='customerorderdetail.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        context['order_obj']=order_obj
        return context
    # ngăn chặn customer thay đổi path trên http để xem thông tin order khác,customer chỉ xem được order mà mình đã đặt
    def dispatch(self,request,**kwargs):
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        if Customer.objects.get(user=request.user)!=order_obj.cart.customer:
            return redirect('ecomapp:customerprofile')
        return super().dispatch(request,**kwargs)
    




# admin------------------------
class AdminLoginView(FormView):
    template_name='adminpages/adminlogin.html'
    form_class=CustomerLoginForm
    success_url=reverse_lazy('ecomapp:adminhome')

    def form_valid(self, form):
        uname=form.cleaned_data.get('username')
        pword=form.cleaned_data.get('password')
        usr=authenticate(username=uname,password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
            messages.success(self.request,'Đăng nhập bằng tài khoản admin thành công!')
            
        else: 
            return render(self.request,self.template_name,{'form':self.form_class,'error1':'Không hợp lệ'})

        return super().form_valid( form)
    

#Truy cập trang admin phải là account admin nếu không phải thì điều hướng ra trang admin-login
class AdminRequiredMixin(object):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin-login/')
        return super().dispatch(request,*args,**kwargs)
    

class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminhome.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['pendingorders']=Order.objects.filter(order_status='Order received').order_by('-id')
        return context
    
# cach 1 
class AdminOrderDetailView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminorderdetail.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        context['order_obj']=order_obj
        context['allstatus']=ORDER_STATUS
        return context
# cach 2
# class AdminOrderDetailView(AdminRequiredMixin,DetailView):
#     template_name='adminpages/adminorderdetail.html'
#     model=Order
#     context_object_name='order_obj'

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['allstatus']=ORDER_STATUS
#         return context


class AdminLogoutView(TemplateView):
    def get(self,request):
        logout(request)
        messages.success(request,'Đăng xuất thành công!')
        return redirect('ecomapp:home')
    
class AdminOrderListView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminorderlist.html'
    def get_context_data(self,**kwargs):
            context=super().get_context_data(**kwargs)
            context['allorders']=Order.objects.all().order_by('-id')
            return context
    
# class AdminOrderStatusChangeView(AdminRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         ord_id=self.kwargs['pk']
#         ord_obj=Order.objects.get(id=ord_id)
#         new_status=request.POST.get('status')
#         ord_obj.order_status=new_status
#         ord_obj.save()
#         return redirect(reverse_lazy('ecomapp:adminorderdetail',kwargs={'pk':ord_id}))
   
class AdminOrderStatusChangeView(AdminRequiredMixin,TemplateView):
    
    def post(self,request,*args,**kwargs):
        
        ord_id=self.kwargs['pk']
        ord_obj=Order.objects.get(id=ord_id)
        new_status=request.POST.get('status')
        ord_obj.order_status=new_status
        ord_obj.save()
        return redirect(reverse_lazy('ecomapp:adminorderdetail',kwargs={'pk':ord_id}))
    
class AdminOrderReceivedView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminorderreceived.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['received_orders']=Order.objects.filter(order_status='Order received').order_by('-id')
        return context
    
class AdminOrderProcessingView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminorderprocessing.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['processing_orders']=Order.objects.filter(order_status='Order processing').order_by('-id')
        return context
class AdminOrderOnDeliveryView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminorderondelivery.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['on_delivery_orders']=Order.objects.filter(order_status='On delivery').order_by('-id')
        return context
class AdminOrderCompletedView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminordercompleted.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['completed_orders']=Order.objects.filter(order_status='Order completed').order_by('-id')
        return context
class AdminOrderCanceledView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminordercanceled.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['canceled_orders']=Order.objects.filter(order_status='Order canceled').order_by('-id')
        return context

class AdminDeleteOrderView(TemplateView):
    def get(self,request,*args,**kwargs):
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        if order_obj:
            order_obj.delete()
        return redirect('ecomapp:adminorderlist')

class SearchView(TemplateView):
    template_name='search.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET.get('keyword')
        results=Product.objects.filter(title__contains=kw)
        print('results',results)
        context['results']=results
        return context

class AdminProductListView(AdminRequiredMixin, TemplateView):   
    template_name='adminpages/adminproductlist.html'  
    
    def get_context_data(self):
        context=super().get_context_data()
        allproducts=Product.objects.all().order_by('-id')
        context['allproducts']=allproducts
        return context

class AdminProductCreateView(AdminRequiredMixin,CreateView):
    template_name='adminpages/adminproductcreate.html'
    form_class=ProductForm
    success_url=reverse_lazy('ecomapp:adminproductlist')

    def form_valid(self,form):
        p=form.save()
        images=self.request.FILES.getlist('images')
        for i in images:
            ProductImage.objects.create(product=p,image=i)
        return super().form_valid(form)