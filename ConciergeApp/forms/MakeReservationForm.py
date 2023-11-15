from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList, makeNumberOfGuestsList, findClosestReservationHour

HOURS = makeHoursList()
GUESTS_CHOICES = makeNumberOfGuestsList()
CLOSEST_RESERVATION_TIME = findClosestReservationHour()
class MakeReservationForm(forms.Form):
    numberOfGuests = forms.ChoiceField(choices=GUESTS_CHOICES, initial="2", widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    datepicker = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control search_filter rounded", "data-date-format": "dd/mm/yyyy"}), input_formats=['%d/%m/%Y'])
    hourFrom = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    hourTo = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
