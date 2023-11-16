from django import forms

from ConciergeApp.models.UserModel import UserModel

class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True, label="Nazwa użytkownika", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=True, label="Hasło", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email')