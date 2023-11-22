import datetime
from typing import Any
from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList, makeNumberOfGuestsList, findClosestReservationHour, validateTodayDate, validateCurrentTime

HOURS = makeHoursList()
GUESTS_CHOICES = makeNumberOfGuestsList()
CLOSEST_RESERVATION_TIME = findClosestReservationHour()
class SearchRestaurantForm(forms.Form):
    datepicker = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control search_filter rounded", "data-date-format": "dd/mm/yyyy"}), input_formats=['%d/%m/%Y'])
    time = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    numberOfGuests = forms.ChoiceField(choices=GUESTS_CHOICES, initial="2", widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control rounded text-start search_filter", "placeholder": "Restauracja"}))
    
    def clean(self) -> dict[str, Any]:
        try:
            super().clean()
            hour, minute = self.cleaned_data['time'].split(":")
            time = datetime.time(int(hour), int(minute))
            self.cleaned_data['combinedDatetime'] = datetime.datetime.combine(self.cleaned_data['datepicker'], time)
            return self.cleaned_data
        except:
            pass
        
    def is_valid(self) -> bool:
        if super().is_valid():
            if self.cleaned_data['combinedDatetime'] > datetime.datetime.now():
                return True
            self.add_error('datepicker', forms.ValidationError("Nie możesz wybrać daty wcześniejszej niż dzisiejsza"))
        return False