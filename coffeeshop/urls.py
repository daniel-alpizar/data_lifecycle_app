from django.contrib import admin
from django.urls import path    
from . import views


urlpatterns = [
    path('', views.home, name='coffeeshop-home'),
    path('transactional-db/', views.TransactionalView, name='transactional_db'),
    path('order-form/', views.OrderFormView, name='order_form'),
]