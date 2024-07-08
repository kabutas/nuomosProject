from django import forms
from django.core.exceptions import ValidationError
from .models import RentalItem, Rental


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['rental_item', 'customer_name', 'customer_email', 'rental_date', 'return_date']
        widgets = {
            'rental_item': forms.Select(attrs={'class': 'form-control selectmenu'}),
            'rental_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rental_item'].choices = [
            (item.id, f'<img src="127.0.0.1:8000{item.image.url}" alt="{item.model}"> {item.brand} {item.model} ({item.year}) - {item.price_per_day} €/day')
            for item in RentalItem.objects.all()
        ]

    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get('rental_date')
        return_date = cleaned_data.get('return_date')

        if rental_date and return_date:
            if return_date < rental_date:
                raise ValidationError("Nuomos pabaigos data negali būti ankstesnė nei pradžios data.")