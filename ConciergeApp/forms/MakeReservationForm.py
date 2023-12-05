import datetime
from django import forms

from ConciergeApp.forms.FormUtils import makeHoursList, makeNumberOfGuestsList, findClosestReservationHour
from ConciergeApp.models import RestaurantModel

HOURS = makeHoursList()
GUESTS_CHOICES = makeNumberOfGuestsList()
CLOSEST_RESERVATION_TIME = findClosestReservationHour()
class MakeReservationForm(forms.Form):
    numberOfGuests = forms.ChoiceField(choices=GUESTS_CHOICES, initial="2", widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    datepicker = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control search_filter rounded", "data-date-format": "dd/mm/yyyy"}), input_formats=['%d/%m/%Y'])
    hourFrom = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))
    hourTo = forms.ChoiceField(choices=HOURS, initial=CLOSEST_RESERVATION_TIME, widget=forms.Select(attrs={"class": "form-select search_filter rounded"}))

    def clean(self):
        try:
            super().clean()
            hourFrom, minuteFrom = self.cleaned_data['hourFrom'].split(":")
            hourTo, minuteTo = self.cleaned_data['hourTo'].split(":")
            datetimeFrom = datetime.datetime.combine(self.cleaned_data['datepicker'], datetime.time(int(hourFrom), int(minuteFrom)))
            datetimeTo = datetime.datetime.combine(self.cleaned_data['datepicker'], datetime.time(int(hourTo), int(minuteTo)))
            self.cleaned_data['combinedDatetimeFrom'] = datetimeFrom
            self.cleaned_data['combinedDatetimeTo'] = datetimeTo
            return self.cleaned_data
        except:
            pass

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        now = datetime.datetime.now()
        if self.cleaned_data['combinedDatetimeFrom'] < now:
            self.add_error("datepicker", forms.ValidationError("Nie możesz rezerwacji na datę wcześniejszą niż obecna"))
            return False
        if self.cleaned_data['combinedDatetimeFrom'] >= self.cleaned_data['combinedDatetimeTo']:
            self.add_error("datepicker", forms.ValidationError("Niepoprawne godziny rezerwacji"))
            return False
        return True