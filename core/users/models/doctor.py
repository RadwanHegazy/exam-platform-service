from django.db import models
from .base import CustomBaseUser

class Doctor (CustomBaseUser) :
    subject =  models.CharField(max_length=300)


    class Meta: 
        verbose_name = ("doctor")
        verbose_name_plural = ("doctors")