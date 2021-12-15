from django.shortcuts import render
from apartment.models import Apartment
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    apartments = Apartment.objects.all().filter(is_available=True).order_by('created_date')

    context = {
        'apartments': apartments,
    }
    return render(request, 'home.html', context)
