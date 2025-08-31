from django.db import models
from .base import CustomBaseUser

class Level (models.Model) : 
    name = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Student (CustomBaseUser) : 
    level = models.ForeignKey(
        Level,
        related_name='students_level',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    id_number = models.BigIntegerField() 

    class Meta: 
        verbose_name = ("student")
        verbose_name_plural = ("students")