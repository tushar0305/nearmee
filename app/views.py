from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


# Route to get the images for the slider
@api_view(['GET'])
def app_images(request):
    if request.method == 'GET':
        images = AppImage.objects.all()
        if images:
            serializer = AppImageSerializer(images, many=True)
            response = {
                "status": 1,
                "message": "success",
                "home": serializer.data,
            }
        else:
            response = {
                "status": 0,
                "message": "No Images found"
            }
    else:
        response = {
            "status": 0,
            "message": "No Get Method"
        }
    return Response(response)


# Get the list of cities
@api_view(['POST'])
def get_cities(request):
    sub_service_id = request.data.get('subServiceId')
    try:
        sub_service = SubService.objects.get(sub_service_id=sub_service_id)
        response = {
            "status": 1,
            "message": "success",
            "androidCities": sub_service.cities
        }
    except SubService.DoesNotExist:
        response = {
            "status": 0,
            "message": "No Cities found"
        }

    return Response(response)


# User Complaints <Working>
@api_view(['POST'])
def complaint(request):
    if request.method == 'POST':
        booking_id = request.data.get('bookingId')
        complaint = request.data.get('complaint')
        if booking_id:
            try:
                booking = ServiceRequest.objects.get(booking_id=booking_id)

                user_complaint = UserComplaint(booking_id=booking, complaint=complaint, status="pending")
                user_complaint.save()
                serializer = UserComplaintSerializer(user_complaint)

                response = {
                    'status': 1,
                    'message': serializer.data
                }

            except Exception as e:
                response = {
                    'status': 0,
                    'message': str(e)
                }
        else:
            response = {
                'status': 0,
                'message': 'Something went wrong'
            }
    else:
        response = {
            'status':0,
            'message': 'POST method required'
        }

    return Response(response)