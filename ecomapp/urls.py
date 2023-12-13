from django.urls import path
from .views import *
app_name='ecomapp'
urlpatterns=[
    # store------------------
    path('',HomeView.as_view(),name='home'),
    path('about/',AboutView.as_view(),name='about'),
    path('contact-us/',ContactView.as_view(),name='contact'),
    path('all-products/',AllProductsView.as_view(),name='allproducts'),
    path('product/<slug:slug>/',ProductDetailView,name='productdetail'),
    path('my-cart/',MyCartView.as_view(),name='mycart'),
    path('wish-list/',WishListView.as_view(),name='wishlist'),
    
    path('add-to-cart-<int:pro_id>/',AddToCartView.as_view(),name='addtocart'),
    path('manage-cart/<int:cp_id>/',ManageCartView.as_view(),name='managecart'),
    path('empty-cart/',EmptyCartView.as_view(),name='emptycart'),
    path('add-to-wishlist-<int:pro_id>/',AddToWishListView.as_view(),name='addtowishlist'),
    path('remove-from-wishlist-<int:wli_id>/',RemoveFromWishListView.as_view(),name='removefromwishlist'),
    path('search/',SearchView.as_view(),name='search'),
# profile
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('register/',CustomerRegistrationView.as_view(),name='customerRegistration'),
    path('logout/',CustomerLogoutView.as_view(),name='customerlogout'),
    path('login/',CustomerLoginView.as_view(),name='customerlogin'),
    path('profile/',CustomerProfileView.as_view(),name='customerprofile'),
    path('profile/order-<int:pk>/',CustomerOrderDetailView.as_view(),name='customerorderdetail'),
    path('forgot-password/',PasswordForgotView.as_view(),name='passwordforgot'),
    path('password-reset/<email>/<token>/',PasswordResetView.as_view(),name='passwordreset'),

# admin------------
    path('admin-login/',AdminLoginView.as_view(),name='adminlogin'),
    path('admin-home/',AdminHomeView.as_view(),name='adminhome'),
    path('admin-order-<int:pk>/',AdminOrderDetailView.as_view(),name='adminorderdetail'),
    path('admin-logout/',AdminLogoutView.as_view(),name='adminlogout'),
    path('admin-all-orders/',AdminOrderListView.as_view(),name='adminorderlist'),
    path('admin-order-<int:pk>-change/',AdminOrderStatusChangeView.as_view(),name='adminorderstatuschange'),

    path('admin-order-received/',AdminOrderReceivedView.as_view(),name='adminorderreceived'),
    path('admin-order-processing/',AdminOrderProcessingView.as_view(),name='adminorderprocessing'),
    path('admin-order-on-delivery/',AdminOrderOnDeliveryView.as_view(),name='adminorderondelivery'),
    path('admin-order-completed/',AdminOrderCompletedView.as_view(),name='adminordercompleted'),
    path('admin-order-canceled/',AdminOrderCanceledView.as_view(),name='adminordercanceled'),

    path('admin-delete-order<int:pk>/',AdminDeleteOrderView.as_view(),name='admindeleteorder'),
    path('admin-product/list/',AdminProductListView.as_view(),name='adminproductlist'),
    path('admin-product/add/',AdminProductCreateView.as_view(),name='adminproductcreate'),

]
