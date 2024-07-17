from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import DateInput

from .models import Rental, RentalItem


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['first_name', 'last_name', 'drivers_license', 'customer_email', 'rental_date', 'return_date']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_rental_date'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_return_date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.reserved_dates = kwargs.pop('reserved_dates', [])
        super(RentalForm, self).__init__(*args, **kwargs)



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    drivers_license = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'drivers_license', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.drivers_license = self.cleaned_data['drivers_license']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, help_text='Required. Enter your username.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter your password.')


class RentalUpdateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['rental_date', 'return_date']

        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StaffRentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['first_name', 'last_name', 'drivers_license', 'customer_email', 'rental_date', 'return_date']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_rental_date'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'id': 'id_return_date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.reserved_dates = kwargs.pop('reserved_dates', [])
        super(StaffRentalForm, self).__init__(*args, **kwargs)
        # self.fields['rental_item'].queryset = RentalItem.objects.all()
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['customer_email'].initial = self.user.email