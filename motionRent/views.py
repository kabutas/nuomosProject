from django.shortcuts import render, get_object_or_404, redirect
from .models import RentalItem, Rental, Location
from .forms import RentalForm


# Create your views here.

def home(request):
    rental_items_count = RentalItem.objects.count()
    rental_locations = Location.objects.all()
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RentalForm()
    context = {
        'rental_items_count': rental_items_count,
        'rental_locations': rental_locations,
        'form': form,
    }
    return render(request, 'home.html', context)


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
    rental_count = rental_items.count()

    if category:
        rental_items = rental_items.filter(category=category)

    context = {
        'rental_items': rental_items,
        'selected_category': category,
        'categories': ['car', 'motorcycle', 'construction_equipment'],
        'rental_count': rental_count,
    }
    return render(request, 'rental_items_list.html', context)


def rental_item_detail(request, pk):
    rental_item = get_object_or_404(RentalItem, pk=pk)
    context = {
        'rental_item': rental_item
    }
    return render(request, 'rental_item_detail.html', context)
