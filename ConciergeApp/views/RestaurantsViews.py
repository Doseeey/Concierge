from django.shortcuts import redirect, render
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
            form = AddRestaurantForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("/")
        else:
            form = AddRestaurantForm()
        return render(request, "RestaurantViews/addRestaurant.html", {"form": form})
    
    @staticmethod
    def restaurantIndexMethod(request):
        if request.method == "POST":
            form = SearchRestaurantForm(request.POST)
            if form.is_valid():
                filterName = form.cleaned_data["name"]
                if filterName:
                    restaurantList = RestaurantModel.objects.filter(name=filterName)
                else:
                    restaurantList = RestaurantModel.objects.all() 
        else:
            form = SearchRestaurantForm()
            restaurantList = RestaurantModel.objects.all()
        
        context = {'restaurants': restaurantList, "form": form}

        return render(request, "RestaurantViews/index.html", context)

    @staticmethod
    def viewSingleRestaurantMethod(request, restaurantId):
        pass