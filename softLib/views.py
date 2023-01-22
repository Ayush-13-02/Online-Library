from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from softLib.models import Book,Comment
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import os
from django.conf import settings
import PyPDF2
#HomePage
def Home(request):
    if request.method == 'GET':
        Bookdata = Book.objects.all()
        catbooks = Book.objects.values('Category')
        catbook = {item['Category'] for item in catbooks}
        data = {
            'Category':catbook,
            'Books': Bookdata
        }
        return render(request,'Books.html',data)
def Bookone(request,rid):
    if request.method == 'GET':
        book = Book.objects.filter(id=rid)
        catbooks = Book.objects.filter(Category = book[0].Category)
        comment = Comment.objects.filter(Book_id = book[0])
        Path = str(settings.BASE_DIR)+'/media/'+str(book[0].pdf)
        filesize = os.path.getsize(Path)
        kb = True
        if(filesize >= pow(1024,2)):
            filesize = round(filesize/pow(1024,2),2)
            kb = False
        
        file = open(Path,'rb')
        pdfreader = PyPDF2.PdfFileReader(file)
        totalpage = pdfreader.numPages
        data = {
            'Category':catbooks,
            'book': book[0],
            'size':filesize,
            'Kb':kb,
            'Page': totalpage,
            'Comment':comment
        }
        
        return render(request,'Comment.html',data)
def Profile(request):
    params = {
        'edit':True,
        'upload':False,
        'save':False
    }

    return render(request,'EProfile.html',params)

def Comments(request,id):
    if request.method =='POST':
        Bookid = Book.objects.filter(id=id)
        Commentby = request.user
        Comments = request.POST.get('Comments')
        if len(Comments)>=4:
            comment = Comment(Book_id=Bookid[0],Commentby=Commentby,Comments=Comments)
            comment.save()
            book = Book.objects.get(id=id)
            book.Review = book.Review+1
            book.save()
        Url = '/book/'+str(id)
        return redirect(Url)

def DeleteComment(request,id):
    CommentId = Comment.objects.filter(id=id)
    ID = CommentId[0].Book_id.id
    Url = '/book/'+str(ID)
    book = Book.objects.get(id=ID);
    book.Review  = book.Review-1
    book.save()
    CommentId.delete()
    # Comment.save()
    return redirect(Url)
def Userupload(request):
    if request.method == 'POST':
        Title = request.POST.get('Title')
        Category = request.POST.get('Category')
        Author = request.POST.get('Author')
        Cover = request.FILES.get('Cover')
        pdf = request.FILES.get('pdf')
        desc = request.POST.get('desc')
        addby = request.user
        book = Book(Title=Title,Author=Author,Category=Category,Addby=addby,Description=desc,image=Cover,pdf=pdf)
        book.save()
        return redirect('/upload')

    if request.method == 'GET':
        myupload = Book.objects.filter(Addby = request.user)
        params = {
            'myupload':myupload,
            'edit':False,
            'upload':True,
            'save':False
        }
        return render(request,'userupload.html',params)
@csrf_protect
@ensure_csrf_cookie
def Login(request):
    if request.method == 'POST':
        loginusernameame = request.POST['email']
        loginpassword = request.POST['pass']
        user = authenticate(username = loginusernameame, password = loginpassword)  
        if user is not None:
            login(request,user)
            # messages.success(request,"Successfully logged In")
            return redirect('/')
        else:
            # messages.error("Email or Password is wrong")
            return redirect('/login')
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