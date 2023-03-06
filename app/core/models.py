""" Database models """

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """ Manager for users """
    def create_user(self,email,password=None, **extra_fields):
        """ create save and return new user """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """ Create and return new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    # inheriting from AbstractBaseUser because it has authentication functionality for user system but no fields.
    # Permissions mixin contains permission functionality features and field needed for permission feautre

    """ user in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    #defines the field that we want to use for authentication, this is how we can replace the username default field that comes with default user model to our custom email field.
    USERNAME_FIELD = "email"
