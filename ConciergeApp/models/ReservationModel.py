from django.db import models

from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.models.UserModel import UserModel

class ReservationModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()