from django.urls import path
from main import views
from django.conf.urls import url

app_name = 'main'
urlpatterns = [
    url('couriers', views.couriers_post),
]