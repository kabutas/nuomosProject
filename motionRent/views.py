from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy

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


class RentalItemListView(ListView):
    model = RentalItem
    template_name = 'rental_items_list.html'
    context_object_name = 'rental_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['rental_items'] = context['rental_items'].filter(category=category)
        context['selected_category'] = category
        context['categories'] = ['car', 'motorcycle', 'construction_equipment']
        context['rental_count'] = context['rental_items'].count()
        return context


class RentalItemDetailView(DetailView):
    model = RentalItem
    template_name = 'rental_item_detail.html'
    context_object_name = 'rental_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rental_item = self.get_object()
        rental = rental_item.rental_set.all().order_by('return_date').first()
        context['return_date'] = rental.return_date if rental else None
        context['now'] = timezone.now().date()
        return context


class RentalCreateView(CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rental_form.html'

    def form_valid(self, form):
        rental_item = get_object_or_404(RentalItem, pk=self.kwargs['pk'])
        form.instance.rental_item = rental_item
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('rental_item_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_item'] = get_object_or_404(RentalItem, pk=self.kwargs['pk'])
        return context
