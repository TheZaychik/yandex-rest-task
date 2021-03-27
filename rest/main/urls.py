from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('couriers', views.couriers_post, name='couriers_post'),
    path('couriers/<int:courier_id>', views.couriers_patch_get, name='couriers_patch_get'),
    path('orders', views.orders_post, name='orders_post'),
    path('orders/assign', views.orders_assign, name='orders_assign'),
    path('orders/complete', views.orders_complete, name='orders_complete'),
]
