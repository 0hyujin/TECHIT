from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

# class User(AbstractUser):
#     phone = models.CharField(verbose_name='전화번호', max_length=11)

class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 값입니다.')
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.sane(using=self._db)
        return user
    
    def create_user(self, username, email =None, password=None, **extra_fields):
        extra_fields.serdefault('is_staff', False)
        extra_fields.serdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    phone = models.CharField(verbose_name='전화번호', max_length=11)
    objects = UserManager()
