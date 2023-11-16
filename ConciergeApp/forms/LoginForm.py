from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Nazwa użytkownika", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=True, label="Hasło", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    