from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timezone, datetime


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='location_images/',
                              blank=True,
                              null=True,
                              default='location_images/no-image-available-building.jpg',
                              )

    def __str__(self):
        return self.name


class RentalItem(models.Model):
    TYPE_CHOICES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
        ('construction_equipment', 'Construction Equipment'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=TYPE_CHOICES)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    number_plate = models.CharField(max_length=12, unique=True, default='XX-XX-XX')
    description = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rental_images/', blank=True, null=True, default='rental_images/no-photo.jpg')

    def __str__(self):
        return f"{self.get_category_display()} - {self.brand} {self.model} ({self.year})"

    def is_available(self):
        latest_rental = self.rental_set.all().order_by('return_date').last()
        return latest_rental is None or latest_rental.return_date < datetime.now().date()


class Rental(models.Model):
    rental_item = models.ForeignKey(RentalItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    drivers_license = models.CharField(max_length=50, default='XX-XX-XX')
    customer_email = models.EmailField()
    rental_date = models.DateField()
    return_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental for: {self.first_name} - ({self.rental_item})"

    def clean(self):
        if self.return_date < self.rental_date:
            raise ValidationError("Return date must be after rental date.")
        # if not self.rental_item.is_available():
        #     raise ValidationError("This item is not available for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
