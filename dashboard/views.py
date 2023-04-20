from django.contrib import messages
from rest_framework.generics import get_object_or_404
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token


User = get_user_model()

def login_view(request):
    csrf_token = get_token(request)
    if request.method == 'POST':
        phone = request.POST['phone']
        otp = request.POST['otp']
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = None

        if user is not None and user.otp == otp:  # Modify this line to match your OTP authentication logic
            if user.is_staff:
                auth_login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Invalid user or staff status.')
        else:
            messages.error(request, 'Invalid phone or OTP.')
    context = {'csrf_token': csrf_token}
    return render(request, 'login/login.html', context)


# Create your views here.
@login_required
def dashboard(request):
    total_complaints = UserComplaint.objects.filter(status="Open").count()
    total_customer = User.objects.filter(is_partner=False).count()
    total_partner = User.objects.filter(is_partner=True).count()

    open = UserComplaint.objects.filter(status="Open").count()
    close = UserComplaint.objects.filter(status="Close").count()
    cancelled = UserComplaint.objects.filter(status="Cancelled").count()

    bookings = ServiceRequest.objects.all()

    return render(request, 'index.html', {'bookings':bookings , 'total_complaints': total_complaints,
                                          'total_customer':total_customer, 'total_partner':total_partner,
                                          'close': close, 'open':open, 'cancelled':cancelled})


def customers(request):
    customers = User.objects.all()
    return render(request, 'customers/customers.html', {'customers': customers})


def partners(request):
    partners = Partner.objects.all()

    return render(request, 'partners/partners.html', {'partners': partners})


def partner_profile(request, id):

    partner = get_object_or_404(Partner, id=id)
    user = partner.profile_token
    address = Address.objects.filter(user=user, is_default=True).first()

    return render(request, 'partners/partner_profile.html', {'partner': partner, 'address':address})


def complaints(request):

    complaints = UserComplaint.objects.select_related('booking_id__profile_token')

    complaint_details = []
    for complaint in complaints:
        # Extract relevant user details from the related profile_token object
        user_details = {
            'first_name': complaint.booking_id.profile_token.first_name,
            'last_name': complaint.booking_id.profile_token.last_name,
            'email': complaint.booking_id.profile_token.email,
            'phone': complaint.booking_id.profile_token.phone,
            'profile_image': complaint.booking_id.profile_token.profile_image,
        }

        # Append user details along with complaint details to the list
        complaint_data = {
            'id': complaint.id,
            'complaint': complaint.complaint,
            'created': complaint.created,
            'updated': complaint.updated,
            'status': complaint.status,
            'user_details': user_details,
        }
        complaint_details.append(complaint_data)

    return render(request, 'complaint/complaints.html', {'complaints': complaint_details})


def complaint_detail(request, id):

    complaint = get_object_or_404(UserComplaint, id=id)

    return render(request, 'complaint/complaint_detail.html', {'complaint': complaint})