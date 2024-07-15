from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

def response_object(message, data=None, success=None, error=None, token=None):


    if token:
        return{
            "success": success,
            "message": message,
            "error": error,
            "data": data,
            "token": token
            
        }

    else:
        return{
            "success": success,
            "message": message,
            "error": error,
            "data": {
                data
            }
        }


@api_view(["POST"])
def create_user(request):

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    phone_number = request.data.get("phone_number")
    full_name = request.data.get("full_name")
    errors = None

    try:
        with transaction.atomic():
            user = User(username=username, email=email, password=password)
            user.set_password(password)
            user.full_clean()
            user.save()

            motorist = Motorist(owner=user,full_name=full_name, phone_number=phone_number)
            motorist.full_clean()
            
            user.save()
            motorist.save()

            token = Token.objects.create(user=user)

    except ValidationError as e:
        if "username" in e.error_dict:
            errors = "Username should be unique"
        if "email" in e.error_dict:
            errors = "Invalid email address"
        if "password" in e.error_dict:
            errors = "Invalid password, a password must be atleast 8 characters with numbers and letters"


        return Response(
            response_object(
                message="Create account attempt failed.",
                success=False,
                error=errors,
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    

    else:
        user_serializer = UserSerializer(user)
        return Response(
            response_object(
                message="Create account attempt successful.",
                data=dict(user_serializer.data),
                success=True,
                token=token.key
            ),
            status=status.HTTP_200_OK
        )

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

class ProcessParking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        space_id = request.data.get('address')
        duriation = request.data.get('duriation')

        parking_space = ParkingSpace.objects.get(space_id=space_id)
        user = request.user

        processed_parking = ParkedInfo.objects.create(
            owner=user,
            parking_space=parking_space,
            duriation=duriation,
            totalParkingTime= int(duriation)
        )

        processed_parking.full_clean()
        processed_parking.save()
        processed_parking_serializer = ParkingInfoSerializer(processed_parking)

        return Response(
            processed_parking_serializer.data,
            status=status.HTTP_200_OK
        )