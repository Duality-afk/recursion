from django.urls import path,include
from HomeModule import views

urlpatterns = [
     path('', views.home, name='home'),
     path('login/',views.login,name='login'),
     path('register/',views.register,name='register'),
     path('products/',views.productCatalog,name='productCatalog'),
     path('productDetail/<str:slug>/',views.productDetail,name='productDeatil'),
     path('logout/', views.logout, name='logout'),
     path('search/', views.search, name='search'),
     path('filter',views.filter,name='filter'),
     path('track',views.track,name='track'),
     path('pastOrders',views.pastOrders,name='pastOrders'),
     path('iframe',views.iframe,name='iframe'),
     path('payment/',views.payment,name='payment'),
]
