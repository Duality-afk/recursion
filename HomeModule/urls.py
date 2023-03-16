from django.urls import path,include
from HomeModule import views

urlpatterns = [
     path('', views.home, name='home'),
     path('login/',views.login,name='login'),
     path('register/',views.register,name='register'),
     path('products/',views.productCatalog,name='productCatalog'),
     path('logout/', views.logout, name='logout'),
     path('cart/',views.cart,name='cart'),
     path('filter',views.filter,name='filter'),
]
