import hashlib
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from partners.serializers import *
from accounts.serializers import *
import base64

# Register Partner <Half Working>
@api_view(['POST'])
def register_partner(request):
    if request.method == 'POST':
        sub_service_id = request.data.get('subServiceId')
        profile_token = request.data.get('profileToken')
        id_proof = request.data.get('idProofDoc')
        office_address = request.data.get('officeAddress')
        service_status = request.data.get('serviceStatus')
        pincode = request.data.get('pincode')
        id_proof_photo_front = request.FILES.get('idProofPhotoFront')
        id_proof_photo_back = request.FILES.get('idProofPhotoBack')
        address_proof = request.data.get('addressProofDoc')
        address_proof_photo_front = request.FILES.get('addressProofPhotoFront')
        address_proof_photo_back = request.FILES.get('addressProofPhotoBack')
        flag_type = request.data.get('flagType')

        if flag_type == 'new':
            partner_token = hashlib.sha1(str(datetime.now().timestamp()).encode()).hexdigest()[:10]
            try:
                service = SubService.objects.get(sub_service_id=sub_service_id)
                profile = User.objects.get(profile_token=profile_token)

                user_obj = User.objects.get(profile_token=profile_token)
                user_obj.is_partner = True
                user_obj.save()

                #save uploaded images
                upload_path1 = 'registerPartnerDocs/addressProofPhotoFront/'
                upload_path2 = 'registerPartnerDocs/addressProofPhotoBack/'
                upload_path3 = 'registerPartnerDocs/idProofPhotoFront/'
                upload_path4 = 'registerPartnerDocs/idProofPhotoBack/'


                partner_obj = Partner(sub_service_id=service, id_proof=id_proof, address_proof=address_proof, partner_token=
                                      partner_token, office_address=office_address, service_status=service_status,
                                      profile_token=profile, partner_status='pending', pincode=pincode)
                partner_obj.save()

                serializer = RegisteredPartnerSerializer(partner_obj)
                response = {'status': 1, 'message': "Partner Successfully Registered", "data": serializer.data}
            except ObjectDoesNotExist:
                response = {'status': 0, 'message': 'Address not found'}
            except Exception as e:
                response = {'status': 0, 'message': str(e)}
        else:
            response = {'status': 0, 'message': 'Post Method Required'}
        return Response(response)


# Get the list of registered partners <working>
@api_view(['POST'])
def get_registered_partners(request):
    sub_service_id = request.data.get('subServiceId')
    if request.method == 'POST':
        try:
            partners = Partner.objects.filter(sub_service_id=sub_service_id).values()
            if partners:
                response = {
                    'status': 1,
                    'message': 'success',
                    'fetchSubServices': list(partners)
                }
            else:
                response = {'status': 0, 'message': 'No Partners found for the given SubService Id'}
        except Service.DoesNotExist:
            response = {'status': 0, 'message': 'SubService does not exist'}
    else:
        response = {'status': 0, 'message': 'POST Method Required'}
    return Response(response)


# Delete Partner <Working Deleting only Partner model not User>
@api_view(['POST'])
def delete_partner(request):
    partner_token = request.data.get('partnerToken')
    profile_token_id = request.data.get('profileTokenId')

    if request.method == 'POST':
        if partner_token:
            try:
                partner = Partner.objects.get(partner_token=partner_token, profile_token__id=profile_token_id)
                partner.delete()

                partner_obj = User.objects.filter(profile_token__id=profile_token_id)
                partner_obj.is_partner = False
                partner_obj.save()

                response = {
                    'status': 1,
                    'message': 'Successfully Deleted'
                }
            except Partner.DoesNotExist:
                response = {
                    'status': 0,
                    'message': 'Partner not found'
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
                'message': 'Please provide partnerToken'
            }
    else:
        response = {
            'status': 0,
            'message': 'POST method required'
        }

    return Response(response)
