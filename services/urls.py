from django.urls import path
from services import views

app_name = 'services'

urlpatterns = [
    path('fetch_services', views.fetch_services, name='fetch_services'),
    path('fetch_sub_services', views.fetch_sub_services, name='fetch_sub_services'),
    path('add_service', views.add_service, name='add_service'),
    path('add_sub_service', views.add_sub_service, name='add_sub_service'),
    path('get_registered_partner_services', views.get_registered_partner_services, name='get_registered_partner_services'),
    path('get_service_request_to_partner', views.get_service_request_to_partner, name='get_service_request_to_partner'),
    path('send_service_request', views.send_service_request, name='send_service_request'),
    path('service_request_view', views.service_request_view, name='service_request_view'),
]
