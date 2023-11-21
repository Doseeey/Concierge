from django import forms

from ConciergeApp.forms.FormUtils import makeGradeList

GRADE_CHOICES = makeGradeList()

class ReviewForm(forms.Form):
    grade = forms.ChoiceField(choices=GRADE_CHOICES, initial="5", widget=forms.Select(attrs={"class": "grade-input"}))
    review = forms.CharField(required=True, label="Zostaw opinię:", widget=forms.TextInput(attrs={"class": "form-control"}))