from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from softLib.models import Book,Comment,Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import os
from django.conf import settings
import PyPDF2
#HomePage
Message=""
Booksearch = Book.objects.none()
Query=""
def Home(request):
    if request.method == 'GET':
        Bookdata = Book.objects.all()
        catbooks = Book.objects.values('Category')
        catbook = {item['Category'] for item in catbooks}
        data = {
            'Category':catbook,
            'Books': Bookdata,
            'Message':Message,
            'Search':Booksearch,
            'query':Query
        }
        return render(request,'Books.html',data)

def Search(request):
    query = request.GET.get('searchbook')
    if len(query)<20 and len(query)>2:
        bookT = Book.objects.filter(Title__icontains=query)
        bookD = Book.objects.filter(Description__icontains=query)
        bookA = Book.objects.filter(Author__icontains=query)
        bookC = Book.objects.filter(Category__icontains=query)
        bookT =  bookT.union(bookD,bookA)
        bookT = bookT.union(bookC)
        global Booksearch
        Booksearch = bookT
    if not Booksearch:
        Booksearch = Book.objects.filter(Category__icontains='Not Found')
        Booksearch = Booksearch[0]
    global Query
    Query = query
    return redirect('/#search')
@login_required
def UpdateProfile(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = email
        bio = request.POST['bio']
        userid = request.user.id
        user = User(id=userid,username=username,email=email,first_name=fname,last_name=lname)
        user.save()
        image = request.POST['profilephoto']
        profile = Profile(user=request.user,image=image,about=bio)
        profile.save()
        print(userid,fname,lname,email,bio)
        return redirect('/profile')

def CloseMessage(request):
    global Message
    Message=""
    return redirect('/')

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
            'Message':Message,
            'Page': totalpage,
            'Comment':comment
        }
        
        return render(request,'Comment.html',data)

@login_required
def EProfile(request):
    params = {
        'edit':True,
        'upload':False,
        'save':False
    }

    return render(request,'EProfile.html',params)

def Downloadbook(request,id):
    global Message
    book = Book.objects.get(id=id)
    book.Downloads = book.Downloads+1
    book.save()
    Url = '/book/'+str(id)
    Message = "Download Successfully"
    return redirect(Url)

@login_required
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

@login_required
def DeleteComment(request,id):
    global Message
    CommentId = Comment.objects.filter(id=id)
    ID = CommentId[0].Book_id.id
    Url = '/book/'+str(ID)
    book = Book.objects.get(id=ID);
    book.Review  = book.Review-1
    book.save()
    CommentId.delete()
    Message = "Comment deleted Successfully"
    # Comment.save()
    return redirect(Url)

@login_required
def Userupload(request):
    global Message
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
        Message = "Book upload Successfully"
        return redirect('/upload')

    if request.method == 'GET':
        myupload = Book.objects.filter(Addby = request.user)
        params = {
            'myupload':myupload,
            'edit':False,
            'upload':True,
            'save':False,
            'Message':Message
        }
        return render(request,'userupload.html',params)

@csrf_protect
@ensure_csrf_cookie
def Login(request):
    global Message
    if request.method == 'POST':
        loginusernameame = request.POST['email']
        loginpassword = request.POST['pass']
        user = authenticate(username = loginusernameame, password = loginpassword)  
        if user is not None:
            login(request,user)
            Message = "Successfully logged In"
            return redirect('/')
        else:
            Message = "Email or Password is wrong"
            return redirect('/login')
    elif request.method == 'GET':
        return render(request,'Login.html')

def Register(request):
    global Message
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
            Message = "Register in EBook Library Successfully"
            return redirect('/')
        else:
            Message = "Register in EBook Library Successfully"
            return redirect('/register')
    elif request.method == 'GET':
        return render(request,'Register.html')

def Logout(request):
    global Message
    logout(request)
    Message = "Logged out Successfully"
    messages.success(request, "Logged out Successfully")
    return redirect('/')