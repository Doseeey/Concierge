from django.apps import apps
from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError


class UserModel(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    
    @staticmethod
    def authenticate(username, password):
        try:
            user = UserModel.objects.get(username=username)
            if user.password == password:
                return True
            else:
                raise ValidationError("Incorrect password")
        except ObjectDoesNotExist as exc:
            raise ValidationError("Incorrect username") from exc
        
    @staticmethod
    def setUser(username):
        apps.get_app_config("ConciergeApp").currentUser = UserModel.objects.get(username=username)
        
    @staticmethod
    def cleanUser():
        apps.get_app_config("ConciergeApp").currentUser = None