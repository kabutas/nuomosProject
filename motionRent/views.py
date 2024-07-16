from datetime import datetime
from io import BytesIO

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy
from PIL import Image, ImageDraw, ImageFont
from django.core.files.images import ImageFile
from .models import RentalItem, Rental, Location
from .forms import RentalForm, RegistrationForm, LoginForm


# Create your views here.
def add_watermark(image):
    base_image = Image.open(image).convert("RGBA")

    # Make the image editable
    txt = Image.new('RGBA', base_image.size, (255, 0, 255, 0))

    # Choose a font and size
    font = ImageFont.truetype('arial.ttf', 15)

    d = ImageDraw.Draw(txt)

    # Position the text at (10, 10) from the top left corner
    d.text((10, 10), "Unavailable", fill=(255, 0, 255, 128), font=font)

    watermarked = Image.alpha_composite(base_image, txt)

    # Save the watermarked image
    byte_arr = BytesIO()
    watermarked.save(byte_arr, format='PNG')
    return byte_arr.getvalue()


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


def about(request):
    return render(request, 'about.html')


class RentalItemListView(ListView):
    model = RentalItem
    template_name = 'rental_items_list.html'
    context_object_name = 'rental_items'

    from django.utils import timezone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        rental_items = context['rental_items']

        if category:
            rental_items = rental_items.filter(category=category)

        # Adding availability status to each rental item
        for item in rental_items:
            rental = item.rental_set.all().order_by('return_date').last()
            if rental:
                item.is_available = rental.return_date < timezone.now().date()
            else:
                item.is_available = True

        # Sorting items to show available ones first
        rental_items = sorted(rental_items, key=lambda x: not x.is_available)

        context['rental_items'] = rental_items
        context['selected_category'] = category
        context['categories'] = ['car', 'motorcycle', 'construction_equipment']
        context['rental_count'] = len(rental_items)

        return context


class RentalItemDetailView(DetailView):
    model = RentalItem
    template_name = 'rental_item_detail.html'
    context_object_name = 'rental_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rental_item = self.get_object()
        rental = rental_item.rental_set.all().order_by('return_date').last()
        context['return_date'] = rental.return_date if rental else None
        context['now'] = timezone.now().date()

        if rental:
            context['is_available'] = rental.return_date < timezone.now().date()
        else:
            context['is_available'] = True

        return context


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rental_form.html'
    login_url = 'login'

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


class LocationDetailView(DetailView):
    model = Location
    template_name = 'location_detail.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.get_object()
        rental_items = RentalItem.objects.filter(location=location)

        # Define a method to check availability
        def is_available(item):
            rental = item.rental_set.all().order_by('return_date').last()
            return rental.return_date < timezone.now().date() if rental else True

        rental_items = sorted(rental_items, key=lambda x: not is_available(x))
        context['rental_items'] = rental_items

        return context


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data.get('full_name')
            user.drivers_license = form.cleaned_data.get('drivers_license')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def all_rentals(request):
    rentals = Rental.objects.all()
    now = timezone.now().date()
    return render(request, 'all_rentals.html', {'rentals': rentals, 'now': now})