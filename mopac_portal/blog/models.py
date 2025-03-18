from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank = True,null = True)
#    author = models.CharField(max_length=20)
    nazwa = models.TextField()
    smiles = models.TextField()
    smiles1 = models.TextField(default = "")
    smiles2 = models.TextField(default = "")
    cieplo = models.FloatField(default = 0)
    energia = models.FloatField(default = 0)
    cieplo1 = models.FloatField(default = 0)
    energia1 = models.FloatField(default = 0)
    cieplo2 = models.FloatField(default = 0)
    energia2 = models.FloatField(default = 0)
    metoda = models.TextField()
    calculated = models.BooleanField(default = False)
    calculations = models.TextField()
    vibration_count = models.IntegerField(default = 0)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
