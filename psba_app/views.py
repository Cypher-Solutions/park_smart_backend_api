from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError


from .models import *

@api_view(["POST"])
def create_user(request):

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    phone_number = request.data.get("phone_number")
    full_name = request.data.get("full_name")

    try:
        user = User(username=username.strip(), email=email, password=password)
        user.set_password(password)
        user.full_clean()
        user.save()

        motorist = Motorist.objects.create(owner=user,full_name=full_name, phone_number=phone_number)
        motorist.full_clean()
        motorist.save()


    except ValidationError as e:
        return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    except IntegrityError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({"content": f"User sucessfuly created!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def login_user(request):
    
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    print(user)

    if user is not None:
        login(request, user)
        return Response({"content": "User logged in successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def logout_user(request):
    logout(request)
    return Response({"content": "User logged out successfully!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    if not user.check_password(old_password):
        return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"content": "new password saved"}, status=status.HTTP_202_ACCEPTED)


# def process_parking(request):
#     slot_id = request.data.get('address')
#     duriation = request.data.get('duriation')
#     parking_number = request.data.get('parking_number')
#     price = request.data.get('price')


#     if request.user.is_authenticated:
#         processed_parking = Parking(
#             address=address,
#             duriation=duriation,
#             parking_status="Ongoing",
#             parking_number=parking_number,
#             price=price,
#             owner=request.user
#         )

#         processed_parking.save()
#         processed_parking_dict = model_to_dict(processed_parking)
#         processed_parking_dict["entryTime"]= processed_parking.entryTime
#         processed_parking_dict["exitTime"]=processed_parking.exitTime

#         return Response([
#             {"message": "Parking slot successifuly booked!"},
#             {"response": processed_parking_dict}], 
#             status=status.HTTP_201_CREATED
#         )
#     else:
#         return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
