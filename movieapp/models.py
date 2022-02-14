from django.db import models
from django.contrib.auth.models import User 
from PIL import Image
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    trailer = models.CharField(max_length=200, null=False)
    year = models.IntegerField(null=False)
    star = models.IntegerField(null=False)
    show =  models.BooleanField(default=True)

    def __str__(self):
        return self.name 

# Profile model with its attributes
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
     

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])
        
    def __str__(self):
        return f' Profile - {self.user.username}'
    