from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

#HomePage
def Home(request):
    if request.method == 'GET':
        return render(request,'Books.html')
def Book(request):
    if request.method == 'GET':
        return render(request,'Book.html')
def Profile(request):
    params = {
        'edit':True,
        'upload':False,
        'save':False
    }

    return render(request,'EProfile.html',params)
 
def Userupload(request):
    params = {
        'edit':False,
        'upload':True,
        'save':False
    }
    return render(request,'userupload.html',params)

def Login(request):
    if request.method == 'POST':
        loginusernameame = request.POST['email']
        loginpassword = request.POST['pass']
        print(loginusernameame,loginpassword)
        user = authenticate(username = loginusernameame, password = loginpassword)
        print("Hello, ",user)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged In")
            return redirect('/')
        else:
            messages.error("Email or Password is wrong")
            return redirect('login')
    elif request.method == 'GET':
        return render(request,'Login.html')

def Register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = email
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            myuser = User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Register in EBook Library Successfully")
            return redirect('/')
        else:
            HttpResponse(request,"Passward doesn't match")
            return redirect('/register')
    elif request.method == 'GET':
        return render(request,'Register.html')

def Logout(request):
    logout(request)
    messages.success(request, "Logged out Successfully")
    return redirect('/')