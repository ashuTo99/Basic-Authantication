from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    username = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    profile_image = models.ImageField(blank=True,null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField( auto_now_add=True)


    def __str__(self) -> str:
        return str(self.email)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    object = UserManager()