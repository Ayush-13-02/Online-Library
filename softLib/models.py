from email.policy import default
from django.db import models

# Create your models here.
class Book(models.Model):
    Title = models.CharField(max_length=150,default="")
    Author = models.CharField(max_length=80,default="")
    Downloads = models.IntegerField(default=0)
    Pages = models.IntegerField(default=0)
    Size = models.FloatField(default=0)
    Description = models.TextField()
    image = models.ImageField(upload_to="images", default="")
    pdf = models.FileField(upload_to="pdf", default="")

    def __str__(self):
        return self.Title