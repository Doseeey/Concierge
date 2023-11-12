from django.shortcuts import render
from django.urls import path

from Concierge.libs.View import View
from ConciergeApp.forms.AddRestaurantForm import AddRestaurantForm
from ConciergeApp.forms.SearchRestaurantForm import SearchRestaurantForm
from ConciergeApp.models.RestaurantModel import RestaurantModel


class RestaurantsViews(View):
    @staticmethod
    def register():
        return [
            path("restaurant/add", RestaurantsViews.addRestaurantMethod, name="addRestaurant"),
            path("", RestaurantsViews.restaurantIndexMethod, name="restaurantSearch"),
            path("restaurant/view/<int:restaurantId>", RestaurantsViews.viewSingleRestaurantMethod, name="viewSingleRestaurant")
        ]
        
    @staticmethod
    def addRestaurantMethod(request):
        if request.method == 'POST':
            form = AddRestaurantForm(request.POST)
            if form.is_valid():
                post = RestaurantModel()
                post.name = request.POST.get('restaurantName')
                post.city = request.POST.get('restaurantCity')
                post.address = request.POST.get('restaurantAddress')
                post.photo_path = request.POST.get('restaurantThumb')
                post.opening_hour = request.POST.get('restaurantFrom')
                post.closing_hour = request.POST.get('restaurantTo')
                post.review = 0  
                post.save()
        else:
            form = AddRestaurantForm()
        return render(request, "RestaurantViews/addRestaurant.html", {"form": form})
    
    @staticmethod
    def restaurantIndexMethod(request):
        if request.method == "POST":
            form = SearchRestaurantForm(request.POST)
            if form.is_valid():
                pass
        else:
            form = SearchRestaurantForm()
            
        restaurantList = RestaurantModel.objects.all()
        context = {'restaurants': restaurantList, "form": form}

        return render(request, "RestaurantViews/index.html", context)
    
    @staticmethod
    def viewSingleRestaurantMethod(request, restaurantId):
        pass