from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from accounts.ACCOUNTS_CONSTANTS import *
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        return self.create_user(phone, password, **other_fields)

    def create_user(self, phone, password, **other_fields):

        if not phone:
            raise ValueError(_('You must provide an phone number'))
        # phone = self.phone
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, unique=True)
    profile_image = models.ImageField(upload_to="user_profile_image/")
    profile_token = models.CharField(max_length=100)
    otp = models.CharField(max_length=20)

    # user status
    is_active = models.BooleanField(default=False, verbose_name='status')
    is_staff = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name_plural = "1. Accounts"

    def __str__(self):
        return self.first_name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="address_profile_token")
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    is_default = models.BooleanField(default=False)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "2. Address"


class Service(models.Model):
    service_id = models.CharField(max_length=55)
    service_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "4. Service"

    def __str__(self):
        return self.service_name


class SubService(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="subservice_service")
    sub_service_id = models.CharField(max_length=55, primary_key=True)
    sub_service_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "5. SubService"

    def __str__(self):
        return self.sub_service_name


class Partner(models.Model):
    city_id = models.CharField(max_length=100)
    is_city_approved = models.BooleanField(default=False)
    office_address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=255)
    id_proof = models.CharField(max_length=255)
    is_id_proof = models.BooleanField(default=False)
    id_proof_front = models.ImageField(upload_to="user_id_proof_image/")
    id_proof_back = models.ImageField(upload_to="user_id_proof_image/")
    address_proof = models.CharField(max_length=255)
    is_address_proof = models.BooleanField(default=False)
    address_proof_front = models.ImageField(upload_to="user_id_address_image/")
    address_proof_back = models.ImageField(upload_to="user_id_address_image/")
    partner_token = models.CharField(max_length=100)
    # city_id = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address")
    service_type_name = models.CharField(max_length=255)
    partner_status = models.CharField(max_length=50, choices=PARTNER_STATUS, default=PARTNER_STATUS_DEFAULT)
    service_status = models.CharField(max_length=50, choices=SERVICE_STATUS, default=SERVICE_STATUS_DEFAULT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    profile_token = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_profile_token')
    sub_service_id = models.ForeignKey(SubService, on_delete=models.PROTECT, related_name='partner_subservice')

    class Meta:
        verbose_name_plural = "3. Partner"

    def __str__(self):
        return self.id_proof


class City(models.Model):
    city = models.CharField(max_length=55)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "6. City"
    
    def __str__(self):
        return self.city


class ServiceRequest(models.Model):
    booking_id = models.CharField(max_length=255)
    # service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="serviceRequest_service_id")
    sub_service_id = models.ForeignKey(SubService, on_delete=models.CASCADE,
                                       related_name="serviceRequest_sub_service_id")
    profile_token = models.ForeignKey(User, on_delete=models.PROTECT, related_name="service_request_profile_token",
                                      default=None)
    partner_token = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name="service_request_partner_token",
                                      default=None)
    date = models.DateField()
    time = models.TimeField()
    additional_details = models.CharField(max_length=500)
    service_request_image_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "7. Service Request"
    
    def __str__(self):
        return self.booking_id


class ServiceRequestImage(models.Model):
    booking_id = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,
                                   related_name="servicerequestimage_booking_id")
    image = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "8. Service Request Images"
    
    def __str__(self):
        return self.booking_id


class AppImage(models.Model):
    objects = None
    image = models.ImageField(upload_to="app_images")
    detail = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "9. App Images"
    
    def __str__(self):
        return self.detail


class UserComplaint(models.Model):
    booking_id = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name="user_complaint_booking_id")
    complaint = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255 ,default="pending")

    class Meta:
        verbose_name_plural = "10. User Complaint"

    def __str__(self):
        return self.complaint
