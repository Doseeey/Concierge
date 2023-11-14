from django.db import models

class RestaurantModel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    review = models.FloatField(default=0.0)
    