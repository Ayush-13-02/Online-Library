from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver
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
    about = models.TextField(null=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.Profile.save()