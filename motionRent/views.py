from django.shortcuts import render, get_object_or_404
from .models import RentalItem, Rental


# Create your views here.


def temporary(request):
    return render(request, 'temporary.html')


# def rental_items_list(request):
#     category = request.GET.get('category')
#     if category:
#         rental_items = RentalItem.objects.filter(category=category)
#     else:
#         rental_items = RentalItem.objects.all()
#     context = {
#         'rental_items': rental_items,
#         'selected_category': category,
#         'categories': ['Car', 'Motorcycle', 'Construction_Equipment']
#     }
#     return render(request, 'rental_items_list.html', context)

def rental_items_list(request):
    category = request.GET.get('category')
    rental_items = RentalItem.objects.all()

    if category:
        rental_items = rental_items.filter(category=category)

    context = {
        'rental_items': rental_items,
        'selected_category': category,
        'categories': ['car', 'motorcycle', 'construction_equipment']
    }
    return render(request, 'rental_items_list.html', context)


def rental_item_detail(request, pk):
    rental_item = get_object_or_404(RentalItem, pk=pk)
    context = {
        'rental_item': rental_item
    }
    return render(request, 'rental_item_detail.html', context)