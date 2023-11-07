from django.db import models

class RestaurantModel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    photo_path = models.CharField(max_length=255)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    review = models.FloatField()
    