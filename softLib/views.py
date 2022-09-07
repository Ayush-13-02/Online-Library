from django.http import HttpResponse
from django.shortcuts import render

#HomePage
def Home(request):
    return render(request,'Home.html')