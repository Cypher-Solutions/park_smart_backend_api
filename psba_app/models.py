from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Motorist(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user"
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)


class ParkingSpace(models.Model):
    type = models.CharField(max_length=10)
    address = models.TextField(max_length = 255)
    price = models.DecimalField(max_digits=1000000, decimal_places=2, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    prepaid = models.BooleanField()
    is_available = models.BooleanField(default=False)
    space_id = models.CharField(max_length=255)


class ParkedInfo(models.Model):
    owner = models.ForeignKey(
        Motorist,
        on_delete=models.CASCADE,
        related_name="parked_motorist"
    )

    parking_space= models.OneToOneField(
        ParkingSpace,
        on_delete=models.CASCADE,
        related_name="parked_space_info",
    )

    duriation = models.CharField(max_length = 20)
    entryTime = models.DateTimeField(auto_now_add=True)
    exitTime = models.DateTimeField(auto_now=True)
    totalParkingTime = models.DecimalField(max_digits=999999, decimal_places=2)

class Favourites(models.Model):
    owner = models.ForeignKey(
        Motorist,
        on_delete=models.CASCADE,
        related_name="fav_motorist"
    )

    parking_space= models.ForeignKey(
        ParkingSpace,
        on_delete=models.CASCADE,
        related_name="fav_space",
    )



class Vehicle(models.Model):
    owner = models.ForeignKey(
        Motorist,
        on_delete=models.CASCADE,
        related_name="motirist_vehicle",
    )
    car_reg = models.CharField(max_length=8, null=False)
    model = models.CharField(max_length=200,)

