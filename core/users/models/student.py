from django.db import models
from .base import CustomBaseUser

class Level (models.Model) : 
    name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Student (CustomBaseUser) : 
    level = models.ForeignKey(
        Level,
        related_name='st_level',
        on_delete=models.SET_NULL,
        null=True
    )
    id_number = models.BigIntegerField() 

    class Meta: 
        verbose_name = ("student")
        verbose_name_plural = ("students")