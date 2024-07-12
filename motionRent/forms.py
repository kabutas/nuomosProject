from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Rental


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['customer_name', 'customer_email', 'rental_date', 'return_date']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RegistrationForm(UserCreationForm):
    drivers_license = forms.CharField(max_length=30,
                                      required=True,
                                      help_text='Required. Enter your driver\'s license number.')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'drivers_license']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, help_text='Required. Enter your username.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter your password.')
