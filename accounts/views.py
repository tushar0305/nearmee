from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
import hashlib, time
from .serializers import *
from .models import *


# User Login <Working>
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        try:
            phone = request.data.get('phone')
            otp = request.data.get('otp')

            if phone and otp:
                user = User.objects.filter(phone=phone).first()
                if user:
                    if user.otp == otp:
                        serializer = UserSerializer(user)
                        response = {
                            'status': 1,
                            'message': 'Successfully logged in',
                            'user': serializer.data
                        }
                    else:
                        response = {
                            'status': 0,
                            'message': 'Invalid OTP'
                        }
                else:
                    response = {
                        'status': 0,
                        'message': 'User not found'
                    }
            else:
                response = {
                    'status': 0,
                    'message': 'Please enter phone and OTP'
                }
        except Exception as e:
            response = {
                'status': 0,
                'message': str(e)
            }
    else:
        response = {
            'status': 0,
            'message': 'Invalid Request'
        }
    return Response(response, status=status.HTTP_200_OK)


# User Register <Working>
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        try:
            first_name = request.data.get('firstName')
            last_name = request.data.get('lastName')
            phone = request.data.get('phone')
            otp = request.data.get('otp')
            email = request.data.get('email')

            if phone:
                if not User.objects.filter(phone=phone).exists():
                    profile_token = hashlib.sha1(
                        str(time.time()).encode('utf-8')).hexdigest()[:10]
                    profile_image = "https://partner.moveonwheels.in/nearMeapis/profileImage/logo.png"
                    user = User(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                profile_image=profile_image, profile_token=profile_token, otp=otp, city_id=1)
                    user.save()
                    serializer = UserSerializer(user)
                    response = {
                        'status': 1,
                        'message': 'Successfully registered',
                        'user': serializer.data
                    }
                else:
                    response = {
                        'status': 0,
                        'message': 'User Already Registered'
                    }
            else:
                response = {
                    'status': 0,
                    'message': 'Please enter mobile number'
                }
        except Exception as e:
            response = {
                'status': 0,
                'message': str(e)
            }
    else:
        response = {
            'status': 0,
            'message': 'Invalid Request'
        }
    return Response(response, status=status.HTTP_200_OK)


# Verify Otp <Working>
@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    if request.method == 'POST':
        try:
            user = User.objects.get(phone=phone, otp=otp)
            user.save()
            serializer = UserSerializer(user)
            response = {
                'status': 1,
                'message': 'success',
                'user': serializer.data
            }
        except User.DoesNotExist:
            response = {
                'status': 0,
                'message': 'Otp you entered is not correct'
            }
    else:
        response = {
            'status': 0,
            'message': 'Please Enter Otp or Phone'
        }

    return Response(response)


# Add User Address <Working>
@api_view(['POST'])
def add_user_address(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        state = request.data.get('state')
        city = request.data.get('city')
        pincode = request.data.get('pincode')
        address = request.data.get('address')

        if profile_token:
            try:
                user = User.objects.get(profile_token=profile_token)
                # Checking if any row with is_default=True already exists
                address_first = Address.objects.filter(user=user, is_default=True).first()

                # If address_first exists, set is_default=False for the new address object
                is_default = False if address_first else True

                address_obj = Address(user=user, state=state, city=city, pincode=pincode,
                                       is_default=is_default, address=address)
                address_obj.save()
                serializer = AddressSerializer(address_obj)

                response = {
                    'status': 1,
                    'message': 'Successfully added address',
                    'address': serializer.data
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
            'status': 0,
            'message': 'Post Method Required'
        }
    return Response(response)


# Delete, Edit, Set Default Address <Working>
@api_view(['POST'])
def user_address(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        address_id = request.data.get('addressId')
        address = request.data.get('address')
        state = request.data.get('state')
        city = request.data.get('city')
        pincode = request.data.get('pincode')
        flag_type = request.data.get('flagType')

        if flag_type == 'editAddress':
            try:
                address_obj = Address.objects.get(user__profile_token=profile_token, id=address_id)
                address_obj.state = state
                address_obj.city = city
                address_obj.pincode = pincode
                address_obj.address = address
                address_obj.save()
                serializer = AddressSerializer(address_obj)
                response = {'status': 1, 'message': 'Successfully updated address', 'data': serializer.data}
            except ObjectDoesNotExist:
                response = {'status': 0, 'message': 'Address not found'}
            except Exception as e:
                response = {'status': 0, 'message': str(e)}
        elif flag_type == 'deleteAddress':
            try:
                address_obj = Address.objects.get(user__profile_token=profile_token, id=address_id)
                address_obj.delete()
                response = {'status': 1, 'message': 'Successfully deleted address'}
            except ObjectDoesNotExist:
                response = {'status': 0, 'message': 'Address not found'}
            except Exception as e:
                response = {'status': 0, 'message': str(e)}
        elif flag_type == 'setDefaultAddress':
            try:
                address_obj = Address.objects.get(user__profile_token=profile_token, id=address_id)
                address_obj.is_default = True
                address_obj.save()
                serializer = AddressSerializer(address_obj)
                response = {'status': 1, 'message': 'Successfully updated address', 'data': serializer.data}
            except ObjectDoesNotExist:
                response = {'status': 0, 'message': 'Address not found'}
            except Exception as e:
                response = {'status': 0, 'message': str(e)}
        else:
            response = {'status': 0, 'message': 'No FlagType Selected'}
    else:
        response = {'status': 0, 'message': 'Post Method Required'}
    return Response(response)


# Get User Profile <Working>
@api_view(['POST'])
def get_user_profile(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        try:
            user = User.objects.get(profile_token=profile_token)
            serializer = UserProfileSerializer(user)
            response = {
                'status': 1,
                'message': 'success',
                'androidProfile': serializer.data
            }
        except User.DoesNotExist:
            response = {
                'status': 0,
                'message': 'No Profile found'
            }
    else:
        response = {
            'status': 0,
            'message': 'No Post Method'
        }
    return Response(response)


# Get User Address <working>
@api_view(['POST'])
def fetch_my_address(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        queryset = Address.objects.filter(user__profile_token=profile_token)
        serializer = AddressSerializer(queryset, many=True)
        if queryset.exists():
            response = {
                'status': 1,
                'message': 'success',
                'fetchMyAddress': serializer.data
            }
        else:
            response = {
                'status': 0,
                'message': 'No Address found'
            }
    else:
        response = {
            'status': 0,
            'message': 'No Method'
        }
    return Response(response)


# Get user order list <working>
@api_view(['POST'])
def get_order_list(request):
    if request.method == 'POST':
        profile_token = request.data.get('profileToken')
        orders = ServiceRequest.objects.filter(profile_token__profile_token=profile_token)
        if orders.exists():
            response = {
                'status': 1,
                'message': 'success',
                'orderFromMe': ServiceRequestSerializer(orders, many=True).data
            }
        else:
            response = {
                'status': 0,
                'message': 'No Order From You'
            }
    else:
        response = {
            'status': 0,
            'message': 'No Post Method'
        }
    return Response(response)
