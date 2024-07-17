from django.urls import path
from django.views.generic import TemplateView

from .views import home, RentalItemListView, RentalItemDetailView, RentalCreateView, LocationDetailView, \
    register, login_view, logout_view, about, all_rentals, rental_detail, rental_update, rental_delete, \
    StaffReservationCreateView

urlpatterns = [
    path('', home, name='home'),
    path('rental-items/', RentalItemListView.as_view(), name='rental_items_list'),
    path('rental-items/<int:pk>/', RentalItemDetailView.as_view(), name='rental_item_detail'),
    path('create-rental/<int:pk>/', RentalCreateView.as_view(), name='create_rental'),
    path('location/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('all_rentals/', all_rentals, name='all_rentals'),
    path('rental/<int:pk>/', rental_detail, name='rental_detail'),
    path('rental/update/<int:rental_id>/', rental_update, name='rental_update'),
    path('rental/delete/<int:rental_id>/', rental_delete, name='rental_delete'),
    path('staff/reservation/new/', StaffReservationCreateView.as_view(), name='staff_reservation_create'),
    path('reservation-success/', TemplateView.as_view(template_name='reservation_success.html'), name='reservation_success'),

]

