import imp
from django.urls import path
from . import views

urlpatterns = [
    path('/',views.Home, name="Home"),
    path('login',views.Login, name="Login")
]