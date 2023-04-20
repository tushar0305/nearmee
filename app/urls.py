from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app_images', views.app_images, name='app_images'),
    path('get_cities', views.get_cities, name='get_cities'),
    path('complaint', views.complaint, name='complaint')
]
