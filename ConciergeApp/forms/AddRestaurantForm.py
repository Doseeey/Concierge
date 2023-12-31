from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList
from ConciergeApp.models.RestaurantModel import RestaurantModel

HOURS = makeHoursList()

class AddRestaurantForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Nazwa restauracji", widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=100, required=True, label="Miasto", widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=100, required=True, label="Adres", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(max_length=255, required=True, label="Opis restauracji", widget=forms.TextInput(attrs={"class": "form-control"}))
    image = forms.ImageField(required=True, label="Zdjęcie restauracji")
    opening_hour = forms.ChoiceField(choices=HOURS, required=True, label="Godzina otwarcia", widget=forms.Select(attrs={"class": "form-select search_filter rounded hour_selector"}))
    closing_hour = forms.ChoiceField(choices=HOURS, required=True, label="Godzina zamknięcia", widget=forms.Select(attrs={"class": "form-select search_filter rounded hour_selector"}))
    
    class Meta:
        model = RestaurantModel
        fields = ('name', 'city', 'address', 'description', 'image', 'opening_hour', 'closing_hour')