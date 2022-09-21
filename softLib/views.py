from django.http import HttpResponse
from django.shortcuts import render

#HomePage
def Home(request):
    return render(request,'Books.html')

def Login(request):
    return render(request,'Login.html')