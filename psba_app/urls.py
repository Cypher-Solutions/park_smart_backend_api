from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("get-authtoken/", obtain_auth_token),
    path("login/", views.login_user, name="login"),
    path("signup/", views.create_user, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    
]