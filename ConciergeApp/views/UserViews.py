from django.urls import reverse, path

from django.apps import apps
from django.shortcuts import redirect, render
from Concierge.libs.View import View

from ConciergeApp.forms.LoginForm import LoginForm
from ConciergeApp.forms.RegisterForm import RegisterForm
from ConciergeApp.forms.ReviewForm import ReviewForm
from ConciergeApp.models.UserModel import UserModel
from ConciergeApp.models.ReservationModel import ReservationModel
from ConciergeApp.models.RestaurantModel import RestaurantModel
from ConciergeApp.views.ViewsUtils import ReservationDisplay

class UserViews(View):
    @staticmethod
    def register():
        return [
            path("login", UserViews.loginMethod, name="login"),
            path("register", UserViews.registerMethod, name="register"),
            path("logout", UserViews.logoutMethod, name="logout"),
            path("reservations", UserViews.userReservationsMethod, name="userReservations"),
            path(r'^delete/(?P<reservation_id>[0-9]+)/$', UserViews.deleteReservation, name="deleteReservation")
        ]
        
    @staticmethod
    def loginMethod(request):
        if request.method != "POST":
            form = LoginForm()
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if UserModel.authenticate(username, password):
                apps.get_app_config("ConciergeApp").currentUser = UserModel.objects.get(username=username)
                return redirect(reverse("restaurantIndex"))
            
        return render(request, "UserViews/forms/loginForm.html", context={"form": form})
    
    @staticmethod
    def registerMethod(request):
        if request.method != "POST":
            form = RegisterForm()
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            apps.get_app_config("ConciergeApp").currentUser = UserModel.objects.get(username=username)
            return redirect(reverse("restaurantIndex"))
            
        return render(request, "UserViews/forms/registerForm.html", context={"form": form})
    
    @staticmethod
    def logoutMethod(request):
        apps.get_app_config("ConciergeApp").currentUser = None
        return redirect(reverse("restaurantIndex"))
    
    @staticmethod
    def userReservationsMethod(request):
        user = apps.get_app_config("ConciergeApp").currentUser

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

                reservationsData.append(rd)

        form = ReviewForm()

        context = {'reservations': reservationsData, 'form': form}

        return render(request, "UserViews/userReservations.html", context=View.getContext(context))
    
    @staticmethod
    def deleteReservation(request, reservation_id=None):
        reservation = ReservationModel.objects.get(id=reservation_id)
        reservation.delete()
        return redirect("userReservations")