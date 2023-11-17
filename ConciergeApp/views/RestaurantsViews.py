from django.shortcuts import redirect, render, get_object_or_404
from django.urls import path

from django.apps import apps
from Concierge.libs.View import View
from ConciergeApp.forms.AddRestaurantForm import AddRestaurantForm
from ConciergeApp.forms.SearchRestaurantForm import SearchRestaurantForm
from ConciergeApp.forms.MakeReservationForm import MakeReservationForm
from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.models.ReservationModel import ReservationModel
from ConciergeApp.models.UserModel import UserModel

import datetime

class RestaurantsViews(View):
    @staticmethod
    def register():
        return [
            path("restaurant/add", RestaurantsViews.addRestaurantMethod, name="addRestaurant"),
            path("", RestaurantsViews.restaurantIndexMethod, name="restaurantIndex"),
            path("restaurant/view/<int:restaurantId>", RestaurantsViews.viewSingleRestaurantMethod, name="viewSingleRestaurant")
        ]
        
    @staticmethod
    def addRestaurantMethod(request):
        if request.method == 'POST':
            form = AddRestaurantForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("restaurantIndex")
        else:
            form = AddRestaurantForm()
        return render(request, "RestaurantViews/addRestaurant.html", context=View.getContext({"form": form}))
    
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

        return render(request, "RestaurantViews/index.html", context=View.getContext(context))

    @staticmethod
    def viewSingleRestaurantMethod(request, restaurantId):
        viewSingleRestaurant = get_object_or_404(RestaurantModel, id=restaurantId)
        
        if request.method == "POST":
            form = MakeReservationForm(request.POST)
            if form.is_valid():
                #Mozna to zrobic jakos inteligentniej
                reservation = ReservationModel()
                date = form.cleaned_data["datepicker"]
                hourFrom = form.cleaned_data["hourFrom"].split(":")
                hourTo = form.cleaned_data["hourTo"].split(":")
                
                dateFrom = datetime.datetime(date.year, date.month, date.day, int(hourFrom[0]), int(hourFrom[1]))
                dateTo = datetime.datetime(date.year, date.month, date.day, int(hourTo[0]), int(hourTo[1]))

                user = apps.get_app_config("ConciergeApp").currentUser

                if user != None:
                    reservation.user = user
                    reservation.restaurant = viewSingleRestaurant
                    reservation.date_from = dateFrom
                    reservation.date_to = dateTo

                    reservation.save()

        else:
            form = MakeReservationForm()

        context = {'restaurant': viewSingleRestaurant, 'form': form}

        return render(request, "RestaurantViews/singleRestaurant.html", context=View.getContext(context))