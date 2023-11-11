from django.shortcuts import render
from django.urls import path

from Concierge.libs.View import View
from ConciergeApp.models import RestaurantModel


class RestaurantsViews(View):
    @staticmethod
    def register():
        return [
            path("restaurant/add", RestaurantsViews.addRestaurantMethod, name="addRestaurant"),
            path("", RestaurantsViews.restaurantSearch, name="restaurantSearch")
        ]
        
    @staticmethod
    def addRestaurantMethod(request):
        if request.method == 'POST':
            post = RestaurantModel()
            post.name = request.POST.get('restaurantName')
            post.city = request.POST.get('restaurantCity')
            post.address = request.POST.get('restaurantAddress')
            post.photo_path = request.POST.get('restaurantThumb')
            post.opening_hour = request.POST.get('restaurantFrom')
            post.closing_hour = request.POST.get('restaurantTo')
            post.review = 0  
            post.save()
            
            return render(request, "RestaurantViews/search.html")

        else:
            return render(request, "RestaurantViews/index.html")
    
    def restaurantSearch(request):
        restaurantList = RestaurantModel.objects.all()
        context = {'restaurants': restaurantList}

        return render(request, "RestaurantViews/search.html", context)