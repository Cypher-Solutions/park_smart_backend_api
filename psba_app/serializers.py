from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class ParkingSpaceSerializer(serializers.ModelField):
     class Meta:
        model = models.ParkingSpace 
        exclude = ["id"]
    

class ParkingInfoSerializer(serializers.ModelField):
     class Meta:
        model = models.ParkedInfo 
        exclude = ["id"]


class FavouritesSerializer(serializers.ModelField):
     class Meta:
        model = models.Favourites 
        exclude = ["id"]


class VehicleSpaceSerializer(serializers.ModelField):
     class Meta:
        model = models.Vehicle 
        exclude = ["id"]

class MotoristSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Motorist
        fields = ['phone_number', 'full_name']

class UserSerializer(serializers.ModelSerializer):
      # motorist = MotoristSerializer(source="user", read_only=True)
   phone_number = serializers.SerializerMethodField()
   full_name = serializers.SerializerMethodField()

   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'phone_number', 'full_name']

   def get_phone_number(self, obj):
      return obj.user.phone_number

   def get_full_name(self, obj):
      return obj.user.full_name