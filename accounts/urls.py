from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('register_user', views.register_user, name='register_user'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('add_user_address', views.add_user_address, name='add_user_address'),
    path('user_address', views.user_address, name='user_address'),
    path('get_user_profile', views.get_user_profile, name='get_user_profile'),
    path('fetch_my_address', views.fetch_my_address, name='fetch_my_address'),
    path('get_order_list', views.get_order_list, name='get_order_list'),
]
