from django.contrib import admin
from .models import Rental, RentalItem, Location
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('email',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.


admin.site.register(Rental)
admin.site.register(RentalItem)
admin.site.register(Location)



