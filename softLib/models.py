from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    Title = models.CharField(max_length=150,default="")
    Author = models.CharField(max_length=80,default="")
    Category = models.CharField(max_length=80,default="")
    Downloads = models.IntegerField(default=0)
    Addby = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    Pages = models.IntegerField(default=0)
    Size = models.FloatField(default=0)
    Description = models.TextField()
    Review = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images")
    pdf = models.FileField(upload_to="pdf")

    def __str__(self):
        return self.Title

class Comment(models.Model):
    Book_id = models.ForeignKey(Book,null=True,on_delete=models.CASCADE)
    Commentby = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    Date =  models.DateField(auto_now=True)
    Comments = models.TextField()
    Like = models.IntegerField(default=0)
    def __str__(self):
        return self.Commentby.first_name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='Profile')
    image = models.ImageField(upload_to="images")
    about = models.TextField()