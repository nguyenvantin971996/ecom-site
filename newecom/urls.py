from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.storeView,name='store'),
    path('cart/',views.cartView,name='cart'),
    path('product/<str:pk>/',views.productView,name='product'),
    path('update/',views.updateCart,name='update'),
    path('delete/',views.deleteCart,name='delete'),
    path('login/',auth_views.LoginView.as_view(template_name='newecom/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='store'),name='logout'),
    path('signin/',views.Signin,name='signin'),
    path('checkout/',views.Checkout,name='checkout'),
]