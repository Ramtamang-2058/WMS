from django.db import models
from django.contrib.auth.models import User


# category

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


#Dustbin

class Dustbin(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    capacity = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


#dustbin Data
class Data(models.Model):
    dustbin = models.ForeignKey(Dustbin, on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)


#vendor

class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    dob = models.CharField(max_length=255, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, null=True, blank=True)
    current_address = models.CharField(max_length=255, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    citizenship_front = models.ImageField(null=True, blank=True)
    citizenship_back = models.ImageField(null=True, blank=True)
    license_photo = models.ImageField(null=True, blank=True)
    vehicle_brand = models.CharField(max_length=255, null=True, blank=True)
    vehicle_color = models.CharField(max_length=255, null=True, blank=True)
    vehicle_number = models.CharField(max_length=255, null=True, blank=True)
    

#notification
class Notification(models.Model):
    options = (
        ('True', 'True'),
        ('False', 'False'),
    )
    dustbin = models.ForeignKey(Dustbin, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=255, choices=options, null=True, blank=True)