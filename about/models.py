from django.contrib.auth.models import User
from django.db import models


def upload_profile_picture(instance, filename):
    return "about/profile_pictures/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename,
                                                             id=instance.id)

def upload_license_picture(instance, filename):
    return "about/license/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename,
                                                             id=instance.id)



# category

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    

#Dustbin

class Dustbin(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
#     capacity = models.FloatField(null=True, blank=True)
#     height = models.FloatField(null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     location = models.PointField(srid=4326) #  # SRID for WGS84 coordinate system
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
    
#     def __str__(self):
#         return self.name


#dustbin Data
class DataR(models.Model):
    distance = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    volume = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.location

#vendor
class Vendor(models.Model):

    options = (
        ('Active', 'Active'),
        ('Block', 'Block'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=255, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, null=True, blank=True)
    current_address = models.CharField(max_length=255, null=True, blank=True)
    license_photo = models.ImageField(null=True, blank=True)
    status = models.CharField(choices=options, max_length=255, null=True, blank=True)
    vehicle_brand = models.CharField(max_length=255, null=True, blank=True)
    vehicle_color = models.CharField(max_length=255, null=True, blank=True)
    vehicle_number = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
    

#notification
class Notification(models.Model):
    data_entry = models.ForeignKey(DataR, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Feedback(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name