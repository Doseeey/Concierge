from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import path

from django.db.models import Q
from django.db.models import Count
from Concierge.libs.View import View
from ConciergeApp.forms.AddRestaurantForm import AddRestaurantForm
from ConciergeApp.forms.SearchRestaurantForm import SearchRestaurantForm
from ConciergeApp.forms.MakeReservationForm import MakeReservationForm
from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.models.ReservationModel import ReservationModel
from ConciergeApp.models.ReviewModel import ReviewModel

import datetime

from ConciergeApp.models.UserModel import UserModel
from ConciergeApp.objects.CollidesChecker import CollidesChecker

class RestaurantsViews(View):
    @staticmethod
    def register():
        return [
            path("restaurant/add", RestaurantsViews.addRestaurantMethod, name="addRestaurant"),
            path("", RestaurantsViews.indexMethod, name="index"),
            path("restaurant/view/<int:restaurantId>", RestaurantsViews.viewSingleRestaurantMethod, name="viewSingleRestaurant")
        ]
        
    @staticmethod
    def addRestaurantMethod(request):
        if request.method == 'POST':
            form = AddRestaurantForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("index")
        else:
            form = AddRestaurantForm()
        return render(request, "RestaurantViews/addRestaurant.html", context=View.getContext({"form": form}))
    
    @staticmethod
    def indexMethod(request):
        restaurantList = RestaurantModel.objects.all()
        
        if request.method == "POST":
            form = SearchRestaurantForm(request.POST)
            if form.is_valid():
                fields = form.clean()
                bookedInSpecifiedTime = ReservationModel.objects\
                    .filter(
                        Q(date_from__lte=fields['combinedDatetime']) &
                        Q(date_to__gte=fields['combinedDatetime'])
                    )\
                    .values("restaurant_id")\
                    .annotate(reservationCount=Count('restaurant_id'))\
                    .order_by()\
                    .filter(reservationCount__gte=2)
                notAvailableRestaurantIds = [query['restaurant_id'] for query in bookedInSpecifiedTime]
                restaurantList = RestaurantModel.objects.filter(
                    ~Q(id__in=notAvailableRestaurantIds) & 
                    Q(name__icontains=fields['name'])
                )
        else:
            form = SearchRestaurantForm()
        
        context = {'restaurants': restaurantList, "form": form}

        return render(request, "RestaurantViews/index.html", context=View.getContext(context))

    @staticmethod
    def viewSingleRestaurantMethod(request, restaurantId):
        restaurant = get_object_or_404(RestaurantModel, id=restaurantId)
        
        if request.method == "POST":
            form = MakeReservationForm(request.POST)
            if form.is_valid():
                reservation = ReservationModel()
                user = UserModel.getCurrentUser()

                startTime = form.cleaned_data['combinedDatetimeFrom'].time()
                endTime = form.cleaned_data['combinedDatetimeTo'].time()
                
                if not(startTime >= restaurant.opening_hour and (endTime >= restaurant.opening_hour and endTime <= restaurant.closing_hour)):
                    form.add_error("datepicker", ValidationError("Restauracja nie jest czynna w tych godzinach"))
                else:
                    combinedDatetimeFrom: datetime.datetime = form.cleaned_data['combinedDatetimeFrom']
                    combinedDatetimeTo: datetime.datetime = form.cleaned_data['combinedDatetimeTo']
                    
                    bookings = ReservationModel.objects.filter(
                        Q(restaurant=restaurant), 
                        Q(date_from__date=combinedDatetimeFrom.date()) |
                        Q(date_from__date=combinedDatetimeTo.date()) |
                        Q(date_to__date=combinedDatetimeFrom.date())
                    )
                    
                    modelToBook = ReservationModel()
                    modelToBook.user = user
                    modelToBook.restaurant = restaurant
                    modelToBook.date_from = combinedDatetimeFrom
                    modelToBook.date_to = combinedDatetimeTo
                    
                    if len(bookings) < 2:
                        modelToBook.save()
                        form.add_error("numberOfGuests", ValidationError("Udało zarezerwować się stolik w podanym terminie"))
                    else:
                        collidesChecker = CollidesChecker(bookings, modelToBook)
                        if collidesChecker.canBeBooked:
                            modelToBook.save()
                            form.add_error("numberOfGuests", ValidationError("Udało zarezerwować się stolik w podanym terminie"))
                        else:
                            form.add_error("datepicker", ValidationError("Nie można zarezerwować stolika w podanym czasie"))                        

        else:
            form = MakeReservationForm()

        reviews = []
        reservations = ReservationModel.objects.filter(restaurant_id=restaurantId)
        for reservation in reservations:
            try:
                review = ReviewModel.objects.get(reservation_id = reservation.id)
            except:
                continue
            reviews.append(review)

        context = {'restaurant': restaurant, 'form': form, 'reviews': reviews}

        return render(request, "RestaurantViews/singleRestaurant.html", context=View.getContext(context))