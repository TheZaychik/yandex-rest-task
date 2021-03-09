from django.urls import path
from main import views
from django.conf.urls import url

app_name = 'main'
urlpatterns = [
    path('couriers', views.couriers_post),
    path('couriers/<int:courier_id>', views.couriers_patch),
]