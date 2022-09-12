import imp
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home, name="Home"),
    path('other',views.Other, name="Other")
]