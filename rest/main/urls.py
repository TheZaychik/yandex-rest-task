from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('couriers', views.couriers_post),
    path('couriers/<int:courier_id>', views.couriers_patch),
    path('orders', views.orders_post),
    path('orders/assign', views.orders_post),
]