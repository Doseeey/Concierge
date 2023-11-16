from django.db import models

from django.core.exceptions import ObjectDoesNotExist


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
        except ObjectDoesNotExist:
            return False