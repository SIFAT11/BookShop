
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city_town = models.CharField(max_length=50)
    postcode_zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    nid_number = models.CharField(max_length=20, blank=True)
    additional_information = models.TextField(blank=True)
    def __str__(self):
        return self.user.username


import random
import string
from django.db import models
from django.contrib.auth.models import User

class Seller_Profile(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    REQUEST_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    
    Sellerusername = models.OneToOneField(User, on_delete=models.CASCADE)
    Seller_Profile = models.ImageField(upload_to='Seller_Profile', blank=True)
    SellerID = models.CharField(max_length=20, unique=True)
    Seller_NID = models.ImageField(upload_to='NID_pics', blank=True)
    address = models.CharField(max_length=100)
    Gmail = models.EmailField(max_length=50)
    city_town = models.CharField(max_length=50)
    postcode_zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField()
    Shop_name = models.CharField(max_length=50)
    request_status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default=PENDING)
    additional_information = models.TextField(blank=True)
    def __str__(self):
        return self.Sellerusername.username

    def generate_seller_id(self):
        number_part = ''.join(random.choices(string.digits, k=4))
        
        letters_part = ''.join(random.choices(string.ascii_uppercase, k=2))
        
        self.SellerID = f"{number_part}-{letters_part}"

    def save(self, *args, **kwargs):
        # Generate seller ID if it's not set already
        if not self.SellerID:
            self.generate_seller_id()
        super().save(*args, **kwargs)