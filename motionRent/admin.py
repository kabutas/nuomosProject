from django.contrib import admin
from .models import Rental, RentalItem, Location

# Register your models here.

admin.site.register(Rental)
admin.site.register(RentalItem)
admin.site.register(Location)



