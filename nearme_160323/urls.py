from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls'), name='accounts'),
    path('',include('services.urls'), name='services'),
    path('',include('app.urls'), name='app'),
    path('', include('partners.urls'), name='partners'),
    path('', include('dashboard.urls'), name='dashboard')
]
