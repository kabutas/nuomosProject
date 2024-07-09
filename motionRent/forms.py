from django import forms
from .models import Rental


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['customer_name', 'customer_email', 'rental_date', 'return_date']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }