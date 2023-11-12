from django.contrib import admin
from django.urls import include, path    
from . import views
from . import plotly_app # Plotly apps need to be imported even though not used on any path
from . import dash_test


urlpatterns = [
    path('', views.Home, name='coffeeshop_home'),
    path('rawdata-db/', views.RawDataDBView, name='rawdata_db'),
    path('order-form/', views.OrderFormSetView, name='order_form'),
    path('orders-db/', views.OrdersDBView, name='orders_db'),
    path('etl-process/', views.ETLView, name='etl_process'),
    path('treemap-chart/', views.TreemapView, name='treemap_chart'),
    path('dash-chart/', views.DashView, name='dash_chart'),
    path('get-product-price/', views.get_product_price, name='get_product_price'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]