from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

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
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rental_images/', blank=True, null=True, default='rental_images/no-photo.jpg')

    def __str__(self):
        return f"{self.get_category_display()} - {self.brand} {self.model} ({self.year})"


class Rental(models.Model):
    rental_item = models.ForeignKey(RentalItem, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    rental_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f"Rental for: {self.customer_name} - ({self.rental_item})"

