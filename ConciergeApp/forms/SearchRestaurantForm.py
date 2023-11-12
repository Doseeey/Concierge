from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList, makeNumberOfGuestsList, findClosestReservationHour

HOURS = makeHoursList()
GUESTS_CHOICES = makeNumberOfGuestsList()
CLOSEST_RESERVATION_TIME = findClosestReservationHour()
class SearchRestaurantForm(forms.Form):
    datepicker = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control search_filter rounded", "data-date-format": "dd/mm/yyyy"}))
    time = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    numberOfGuests = forms.ChoiceField(choices=GUESTS_CHOICES, initial="2", widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control rounded text-start search_filter", "placeholder": "Restauracja"}))
    