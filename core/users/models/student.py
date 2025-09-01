from django.db import models
from .base import CustomBaseUser

class Student (CustomBaseUser) : 
    level = models.IntegerField()
    id_number = models.BigIntegerField() 

    class Meta: 
        verbose_name = ("student")
        verbose_name_plural = ("students")