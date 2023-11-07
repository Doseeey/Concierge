from django.db import models

from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.models.UserModel import UserModel

class ReservationModel(models.Model):
    user = models.ManyToManyField(UserModel)
    restaurant = models.ManyToManyField(RestaurantModel)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()