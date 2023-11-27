from django.urls import path

from django.apps import apps
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from Concierge.libs.View import View

from ConciergeApp.forms.ReviewForm import ReviewForm
from ConciergeApp.models.ReservationModel import ReservationModel
from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.models.ReviewModel import ReviewModel
from ConciergeApp.models.UserModel import UserModel
from ConciergeApp.views.ViewsUtils import ReservationDisplay

class ReservationsViews(View):
    @staticmethod
    def register():
        return [
            path("reservations", ReservationsViews.userReservationsMethod, name="userReservations"),
            path('delete/<int:reservation_id>', ReservationsViews.deleteReservationMethod, name="deleteReservation")
        ]
        
    @staticmethod
    def userReservationsMethod(request):
        user = UserModel.getCurrentUser()

        if user != None:
            reservations = ReservationModel.objects.filter(user_id=user.id)

            reservationsData = []
            for reservation in reservations:
                restaurantName = RestaurantModel.objects.get(id=reservation.restaurant_id).name

                rd = ReservationDisplay()
                rd.id = reservation.id
                rd.restaurantName = restaurantName
                rd.date = reservation.date_from.date().isoformat()
                rd.timeFrom = reservation.date_from.time().isoformat()
                rd.timeTo = reservation.date_to.time().isoformat()

                try:
                    review = ReviewModel.objects.get(reservation_id=reservation.id)
                    rd.grade = review.grade
                    rd.textReview = review.description
                except ReviewModel.DoesNotExist:
                    review = None
                    rd.grade = review

                reservationsData.append(rd)

            if request.method != "POST":
                form = ReviewForm()
            else: 
                form = ReviewForm(request.POST)
                
                if form.is_valid():
                    reservation = ReservationModel.objects.get(id=int(request.POST.get("id")))
                    review = ReviewModel()
                    review.reservation = reservation
                    review.grade = int(form.cleaned_data["grade"])
                    review.description = form.cleaned_data["review"]

                    review.save()

                    restaurantId = reservation.restaurant.id
                    restaurant = RestaurantModel.objects.get(id=restaurantId)
                    oldGrade = restaurant.review
                    noReviews = restaurant.numberOfReviews+1
                    restaurant.numberOfReviews = noReviews
                    restaurant.review = oldGrade + ((review.grade - oldGrade)/noReviews)
                    restaurant.save()

                    return redirect("userReservations")

            context = {'reservations': reservationsData, 'form': form}

            return render(request, "UserViews/userReservations.html", context=View.getContext(context))
        
        else:
            return redirect("login")
    
    @staticmethod
    def deleteReservationMethod(request, reservation_id=None):
        reservation = ReservationModel.objects.get(id=reservation_id)
        restaurant = reservation.restaurant
        
        try:
            review = ReviewModel.objects.get(reservation_id=reservation_id)
            oldGrade = restaurant.review
            noReviews = restaurant.numberOfReviews-1
            if noReviews != 0:
                restaurant.numberOfReviews = noReviews
                restaurant.review = oldGrade - ((review.grade - oldGrade)/noReviews)
                restaurant.save()
            else:
                restaurant.numberOfReviews = 0
                restaurant.review = 0.0
                restaurant.save()
        except ObjectDoesNotExist:
            pass

        reservation.delete()
        return redirect("userReservations")