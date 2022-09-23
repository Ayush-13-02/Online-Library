import imp
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home, name="Home"),
    path('profile',views.Profile, name="Profile"),
    path('login',views.Login, name="Login"),
    path('logout',views.Logout, name="Logout"),
    path('register',views.Register, name="Register")
]