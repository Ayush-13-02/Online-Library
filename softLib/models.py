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
    image = models.ImageField(upload_to="images")
    pdf = models.FileField(upload_to="pdf")

    def __str__(self):
        return self.Title