from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from ConciergeApp.models.ReservationModel import ReservationModel

class ReviewModel(models.Model):
    reservation = models.OneToOneField(ReservationModel, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    description = models.CharField(max_length=255)