from django.urls import path
from .views import home, temporary, RentalItemListView, RentalItemDetailView, RentalCreateView, LocationDetailView, \
    register, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('temporary/', temporary, name='temporary'),
    path('rental-items/', RentalItemListView.as_view(), name='rental_items_list'),
    path('rental-items/<int:pk>/', RentalItemDetailView.as_view(), name='rental_item_detail'),
    path('create-rental/<int:pk>/', RentalCreateView.as_view(), name='create_rental'),
    path('location/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]