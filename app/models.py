from django.db import models

class Registerdetail(models.Model):
    username=models.CharField(max_length=50)
    useremail=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    

class pangresdata(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    marks=models.IntegerField()
    grade=models.CharField(max_length=50)