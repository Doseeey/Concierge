from django.db import models

from ConciergeApp.models.ReservationModel import ReservationModel

class ReviewModel(models.Model):
    reservation = models.OneToOneField(ReservationModel)
    grade = models.IntegerField()
    description = models.CharField(max_length=255)