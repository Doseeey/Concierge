from django.shortcuts import render
from django.urls import path

from Concierge.libs.View import View


class RestaurantsViews(View):
    @staticmethod
    def register():
        return [
            path("restaurant/add", RestaurantsViews.addRestaurantMethod, name="addRestaurant")
        ]
        
    @staticmethod
    def addRestaurantMethod(request):
        return render(request, "RestaurantViews/index.html")