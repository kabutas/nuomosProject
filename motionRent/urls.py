
from django.urls import path
from .views import temporary, rental_items_list, rental_item_detail, home

urlpatterns = [
    path('', home, name='home'),
    path('rental_items_list/', rental_items_list, name='rental_items_list'),
    path('rental_item_detail/<int:pk>/', rental_item_detail, name='rental_item_detail'),
    # path('rental_items/<int:pk>/', rental_item_detail, name='rental_item_detail')
]

