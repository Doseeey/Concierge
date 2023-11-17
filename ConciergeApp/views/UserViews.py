from django.forms import ValidationError
from django.urls import reverse, path

from django.apps import apps
from django.shortcuts import redirect, render
from Concierge.libs.View import View

from ConciergeApp.forms.LoginForm import LoginForm
from ConciergeApp.forms.RegisterForm import RegisterForm
from ConciergeApp.models.UserModel import UserModel

class UserViews(View):
    @staticmethod
    def register():
        return [
            path("login", UserViews.loginMethod, name="login"),
            path("register", UserViews.registerMethod, name="register"),
            path("logout", UserViews.logoutMethod, name="logout"),
        ]
        
    @staticmethod
    def loginMethod(request):
        if request.method != "POST":
            form = LoginForm()
        else:
            form = LoginForm(request.POST)
            
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                try:
                    UserModel.authenticate(username, password)
                    UserModel.setUser(username)
                    return redirect(reverse("restaurantIndex"))
                except ValidationError as exc:
                    form.add_error(field=None, error=exc)
            
        return render(request, "UserViews/forms/loginForm.html", context={"form": form})
    
    @staticmethod
    def registerMethod(request):
        if request.method != "POST":
            form = RegisterForm()
        else:
            form = RegisterForm(request.POST)
            
            if form.is_valid():
                username = form.cleaned_data['username']
                form.save()
                UserModel.setUser(username)
                return redirect(reverse("restaurantIndex"))
            
        return render(request, "UserViews/forms/registerForm.html", context={"form": form})
    
    @staticmethod
    def logoutMethod(request):
        UserModel.cleanUser()
        return redirect(reverse("restaurantIndex"))
