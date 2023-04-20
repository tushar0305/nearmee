from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('partners/', views.partners, name='partners'),
    path('partners/<int:id>/',views.partner_profile, name='partner_profile'),
    path('complaints/', views.complaints, name='complaints'),
    path('complaint/<int:id>/',views.complaint_detail, name='complaint_detail'),
    path('login_view/', views.login_view, name='login_view'),
]