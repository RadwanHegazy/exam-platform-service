from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager (BaseUserManager) : 

    def create_user(self, password, **kwargs) : 
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, **kwargs) : 
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self.create_user(**kwargs)
    

class CustomBaseUser (AbstractUser) :
    objects = CustomUserManager()

    username = None
    user_permissions = None
    groups = None

    full_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.full_name