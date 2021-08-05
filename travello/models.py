

# Create your models here.
from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Destination(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='pics')
    desc=models.TextField()
    price=models.IntegerField()
    offer=models.BooleanField(default=False)

class Details(models.Model):
    wallet=models.IntegerField(default=5000)
    names=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    places=models.CharField(max_length=1000)


    