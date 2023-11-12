from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList

HOURS = makeHoursList()

class AddRestaurantForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nazwa restauracji", widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=100, required=True, label="Miasto", widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=100, required=True, label="Adres", widget=forms.TextInput(attrs={"class": "form-control"}))
    image = forms.ImageField(required=True, label="Zdjęcie restauracji")
    openingHour = forms.ChoiceField(choices=HOURS, required=True, label="Godzina otwarcia", widget=forms.Select(attrs={"class": "form-select search_filter rounded hour_selector"}))
    closingHour = forms.ChoiceField(choices=HOURS, required=True, label="Godzina zamknięcia", widget=forms.Select(attrs={"class": "form-select search_filter rounded hour_selector"}))