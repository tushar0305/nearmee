from django.urls import path
from partners import views

app_name = 'partners'

urlpatterns = [
    path('register_partner', views.register_partner, name='register_partner'),
    path('get_registered_partners', views.get_registered_partners, name='get_registered_partners'),
    path('delete_partner', views.delete_partner, name='delete_partner')
]
