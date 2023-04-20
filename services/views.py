from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
import hashlib, time, os, random


# To fetch all the services <Working>
@api_view(['GET'])
def fetch_services(request):
    if request.method == 'GET':
        services = Service.objects.all()
        if services:
            serializer = ServiceSerializer(services, many=True)
            response = {
                'status': 1,
                'message': 'success',
                'fetchServices': serializer.data
            }
        else:
            response = {'status': 0, 'message': 'No Services found'}
    else:
        response = {'status': 0, 'message': 'No Get Method'}
    return Response(response)


# To fetch all the sub-services <Working>
@api_view(['POST'])
def fetch_sub_services(request):
    if request.method == 'POST':
        service_id = request.data.get('serviceId')
        try:
            service = Service.objects.get(service_id=service_id) # Get the Service object
            subservices = SubService.objects.filter(service_id=service).values()
            if subservices:
                response = {
                    'status': 1,
                    'message': 'success',
                    'fetchSubServices': list(subservices)
                }
            else:
                response = {'status': 0, 'message': 'No SubServices found for the given serviceId'}
        except Service.DoesNotExist:
            response = {'status': 0, 'message': 'Service with the given serviceId does not exist'}
    else:
        response = {'status': 0, 'message': 'POST Method Required'}
    return Response(response)


# add New Service <Working>
@api_view(['POST'])
def add_service(request):
    if request.method == 'POST':
        service_name = request.data.get("serviceName")
        rand_id = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()[:10]
        prefix = 'nearMe'
        service_id = prefix + rand_id
        if service_name:
            try:
                service = Service(service_id=service_id, service_name=service_name)
                service.save()
                response = {
                    'status': 1,
                    'message': 'Successfully added Service'
                }
            except Exception as e:
                response = {
                    'status': 0,
                    'message': 'Something Went Wrong',
                    'error': str(e)
                }
        else:
            response = {
                'status': 0,
                'message': 'Please enter service name'
            }
    else:
        response = {
            'status': 0,
            'message': 'POST Method Required'
        }
    return Response(response)


# add New SubService <Working>
@api_view(['POST'])
def add_sub_service(request):
    if request.method == 'POST':
        sub_service_name = request.data.get("subServiceName")
        service_id = request.data.get("serviceId")
        sub_id = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()[:10]
        prefix = 'sub'
        sub_service_id = prefix + sub_id

        if sub_service_id:
            try:
                service = Service.objects.get(service_id=service_id) # Get the Service object
                sub_service = SubService(sub_service_id=sub_service_id, service_id=service,
                                         sub_service_name=sub_service_name)
                sub_service.save()
                response = {
                    'status': 1,
                    'message': 'Successfully added sub service'
                }
            except Service.DoesNotExist:
                response = {
                    'status': 0,
                    'message': 'Service with the given serviceId does not exist'
                }
            except Exception as e:
                response = {
                    'status': 0,
                    'message': 'Something went wrong',
                    'error': str(e)
                }
        else:
            response = {
                'status': 0,
                'message': 'Service Id Not Generated'
            }
    else:
        response = {
            'status': 0,
            'message': 'POST Method Required'
        }

    return Response(response)


# get registered partners services <Working>
@api_view(['POST'])
def get_registered_partner_services(request):
    if request.method == 'POST':
        partner_token = request.data.get('partnerToken')
        partner = Partner.objects.filter(partner_token=partner_token).first()
        if partner:
            sub_services = SubService.objects.filter(partner_subservice=partner)
            serializer = SubServiceSerializer(sub_services, many=True)
            response = {
                'status': 1,
                'message': 'success',
                'myservices': serializer.data
            }
        else:
            response = {
                'status': 0,
                'message': 'No Services found'
            }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            'status': 0,
            'message': 'No Post Method'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Get the services requested to partners <Not Working>
@api_view(['POST'])
def get_service_request_to_partner(request):
    if request.method == 'POST':
        partner_token_id = request.data.get('partnerTokenId')
        # Filter ServiceRequest objects based on partner_token field
        orders = ServiceRequest.objects.filter(partner_token__partner_token=partner_token_id).values()
        if orders:
            serializer = ServiceRequestSerializer(orders, many=True)
            response = {
                'status': 1,
                'message': 'success',
                'orderToMe': serializer.data
            }
        else:
            response = {
                'status': 0,
                'message': 'No Order To You'
            }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            'status': 0,
            'message': 'No Post Method'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Send Service Request to partners by user <working>
@api_view(['POST'])
def send_service_request(request):
    sub_service_id = request.data.get('subServiceId')
    profile_token = request.data.get('profileToken')
    partner_token = request.data.get('partnerToken')
    # service_type_name = request.data.get('serviceTypeName')
    date = request.data.get('date')
    time = request.data.get('time')
    additional_details = request.data.get('additionalDetails')
    image1 = request.FILES.get('image1')

    # Generate bookingId
    prefix = 'req'
    count = hashlib.sha1(str(datetime.now().timestamp()).encode()).hexdigest()[:10]
    booking_id = prefix + count

    upload_path1 = 'partnerSearchImages/'
    upload_url1 = 'https://partner.moveonwheels.in/nearMeapis/' + upload_path1

    if request.method == 'POST':
        if sub_service_id:

            user = User.objects.get(profile_token=profile_token)
            partner = Partner.objects.get(partner_token=partner_token)
            sub_service = SubService.objects.get(sub_service_id=sub_service_id)
            try:
                sub_service = SubService.objects.get(sub_service_id=sub_service_id)
                user = User.objects.get(profile_token=profile_token)  # Retrieve User instance based on profile_token
                service_request = ServiceRequest.objects.create(
                    booking_id=booking_id,
                    sub_service_id=sub_service,
                    profile_token=user,  # Assign the retrieved User instance
                    partner_token=partner,
                    date=date,
                    time=time,
                    additional_details=additional_details,
                    service_request_image_id=upload_url1,
                )
                serializer = ServiceRequestSerializer(service_request)
                response = {
                    'status': 1,
                    'message': 'Successfully sent Request',
                    'data': serializer.data
                }
            except Exception as e:
                response = {
                    'status': 0,
                    'message': str(e),
                }
        else:
            response = {
                'status': 0,
                'message': 'Service Not Found',
            }
    else:
        response = {
            'status': 0,
            'message': 'Post Method Required',
        }

    return Response(response)


# Get user service requests <Working>
@api_view(['POST'])
def service_request_view(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        service_requests = ServiceRequest.objects.filter(profile_token__profile_token=profile_token)  # Filter by profile_token
        serializer = ServiceRequestSerializer(service_requests, many=True)  # Serialize queryset to ServiceRequestSerializer
        if service_requests.exists():
            response = {
                'status': 1,
                'message': 'success',
                'serviceRequests': serializer.data  # Include the serialized service requests data in the response
            }
        else:
            response = {'status': 0, 'message': 'No Service Requests found for the given profile token'}
    else:
        response = {'status': 0, 'message': 'No POST Method'}
    return Response(response, status=status.HTTP_200_OK)
