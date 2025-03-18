from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.conf import settings

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    
    car_manufacturer = models.CharField(max_length=100, default='')
    car_model = models.CharField(max_length=100, default='')
    trim = models.CharField(max_length=100, blank=True, null=True, default='')
    regional_spec = models.CharField(max_length=25, default='')
    make_year = models.IntegerField(default=datetime.now().year)
    kilometer_driven = models.IntegerField(blank=True, null=True, default=0)
    body_type = models.CharField(max_length=100, blank=True, null=True, default='')
    is_insured = models.BooleanField(default=False)
    expected_selling_price = models.IntegerField(default=0)
    car_owner_phone_number = models.IntegerField(default=0, blank=True, null=True)
    car_city = models.CharField(max_length=50, default='')
    listing_title = models.CharField(max_length=200, default='')
    tour_url = models.URLField(max_length=400, blank=True, null=True, default='')
    car_description = models.TextField(blank=True, null=True, default='')
    fuel_type = models.CharField(max_length=25, default='')
    transmission_type = models.CharField(max_length=25, default='')
    seating_capacity = models.CharField(max_length=25, blank=True, null=True, default='')
    horsepower = models.CharField(max_length=25, default='')
    engine_capacity = models.CharField(max_length=25, blank=True, null=True, default='')
    steering_side = models.CharField(max_length=25, default='')
    
    # Extras
    climate_control = models.BooleanField(default=False)
    dvd_player = models.BooleanField(default=False)
    keyless_entry = models.BooleanField(default=False)
    navigation_system = models.BooleanField(default=False)
    premium_sound_system = models.BooleanField(default=False)
    cooled_seats = models.BooleanField(default=False)
    front_wheel_drive = models.BooleanField(default=False)
    leather_seats = models.BooleanField(default=False)
    parking_sensors = models.BooleanField(default=False)
    rear_view_camera = models.BooleanField(default=False)
    
    car_location = models.CharField(max_length=200, blank=True, null=True, default='')
    
    vehicle_type = models.CharField(max_length=25,default='')
    is_approved = models.BooleanField(default=False)
    class Meta:
        ordering = ('listing_title',)

    def __str__(self):
        return self.listing_title
    def save(self, *args, **kwargs):
        # Automatically set the listing_title based on year, make, model, and trim
        self.update_listing_title()
        super().save(*args, **kwargs)

    def update_listing_title(self):
        title_components = [
            str(self.make_year),
            self.car_manufacturer,
            self.car_model,
            self.trim
        ]
        # Filter out any empty components
        title_components = [component for component in title_components if component]
        # Join the components with spaces
        self.listing_title = ' '.join(title_components)

    @classmethod
    def update_all_listing_titles(cls):
        for car in cls.objects.all():
            car.update_listing_title()
            car.save()

class CarImage(models.Model):
    image = models.ImageField(upload_to='car/car_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"Image for {self.car.listing_title if self.car else 'Unassigned'}"


# To set privacy policies from the admin area.
class Privacy(models.Model):
    privacy_policy = models.TextField()

    def __str__(self):
        # responsible to show name of carin admin instead of object1
        # also look the authoradmin class in admin.py 
        return self.privacy_policy
    class Meta:
        verbose_name_plural = "Privacy"

#To display some advertisement images
class Ads(models.Model):

    popup_ad = models.ImageField(upload_to='car/car_images/', blank=True, null=True)
    popup_ad_url = models.URLField(max_length=400, blank=True, null = True )
    ad1 = models.ImageField(upload_to='car/car_images/', blank=True, null=True)
    ad1_url = models.URLField(max_length=400, blank=True, null = True )
    ad2 = models.ImageField(upload_to='car/car_images/', blank=True, null=True)
    ad2_url = models.URLField(max_length=400, blank=True, null = True )


    def __str__(self):
        # responsible to show name of carin admin instead of object1
        # also look the authoradmin class in admin.py 
        return str(self.popup_ad)
    
    class Meta:
        verbose_name_plural = "Ads"

    



    
#clients, are the users that try to access car information
#They are not required to login and register with email and password
#They are required to submit phone number for otp verification
class Client(models.Model):
    name = models.CharField( max_length=100,default="-",blank=True, null = True)
    phone_number = models.IntegerField(default=0)


    def __str__(self):
        # responsible to show name of car in admin instead of object1
        # also look the authoradmin class in admin.py 
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Client Phone Number"

class LicensePlate(models.Model):
    city = models.CharField(max_length=100, default="All cities")
    code = models.CharField(max_length=100, default="All codes")
    digits = models.CharField(max_length=100, default="Any digits")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    number = models.CharField(max_length=100, default="Any number", blank=True, null=True)
    plate_format = models.CharField(max_length=100, default="Any format", blank=True, null=True)

    def __str__(self):
        return f"{self.city} - {self.code} - {self.digits} - {self.number}"

# Sample data for LicensePlate model
