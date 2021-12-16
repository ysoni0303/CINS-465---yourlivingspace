from django.http.response import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from slugify import slugify 

from checkout.models import Application
from apartment.models import Apartment
from .models import Apartment, Review
from category.models import Category
from checkout.forms import ApplicationForm
from .forms import ReviewForm, ApartmentForm, ApartmentFormForSaving

def apartment(request):
    p = request.GET.get('page')
    categories = Category.objects.filter()
    total_apartments = Apartment.objects.filter(is_available=True).order_by('-id')
    paginator = Paginator(total_apartments, 4)

    apartments = paginator.get_page(p)
    total_apartments = total_apartments.count()

    context = {
        'apartments': apartments,
        'count': total_apartments,
        'categories' : categories
    }
    return render(request, 'apartment/apartment.html', context)

@login_required(login_url = 'login')
def apartment_add(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        slug = slugify(name)
        updated_request = request.POST.copy()
        updated_request.update({'slug': slug})
        # print('request.FILES',request.FILES )
        print('request.POST', request.POST.get("name"))
        print('updated_request', updated_request)
        
        form = ApartmentFormForSaving(updated_request, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Apartment Added Successful')
            return redirect('apartment_add')
    else:
        form = ApartmentForm()

    context = {
        'form': form,
    }

    return render(request, 'apartment/apartment_add.html', context)

@login_required(login_url='login')
def manage_request(request):
    applications = Application.objects.filter(is_ordered=True).order_by('-created_at')
    context = {
        'applications': applications,
    }
    return render(request, 'apartment/manage_request.html', context)

@login_required(login_url='login')
def update_status(request, id):
    application = Application.objects.get(id=id)
    form = ApplicationForm(instance=application)
    if request.method == 'POST':
        print('IT IS A POST')
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('manage_request')

    context = {'form':form, 'id': id}
    return render(request, 'apartment/update_status.html', context)

def apartmentListing(request, slug=None):
    p = request.GET.get('page')
    all_categories = Category.objects.filter()
    categories = get_object_or_404(Category, slug=slug)
    total_apartments = Apartment.objects.filter(category=categories, is_available=True).order_by('-id')
    paginator = Paginator(total_apartments, 4)

    apartments = paginator.get_page(p)
    total_apartments = total_apartments.count()

    context = {
        'apartments': apartments,
        'count': total_apartments,
        'categories': all_categories
    }

    return render(request, 'apartment/apartment.html', context)


def apartment_view(request, slug=None, apartment_slug=None):
    try:
        apartment = Apartment.objects.get(category__slug=slug, slug=apartment_slug)
    except Exception as e:
        raise e
    
    all_reviews = Review.objects.filter(apartment_id=apartment.id, status=True)

    context = {
        'apartment': apartment,
        'reviews': all_reviews,
    }

    return render(request, 'apartment/apartment_view.html', context)

@login_required(login_url = 'login')
def submit_review(request, apartment_id):
    url = request.META.get('HTTP_REFERER')
    print('url', url)
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user__id=request.user.id, apartment__id=apartment_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.apartment_id = apartment_id
                data.user_id = request.user.id
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect(url)

def search(request):
    if 'keyword' in request.GET:
        word = request.GET['keyword']
        if word:
            apartments = Apartment.objects.order_by('-created_date').filter(Q(description__icontains=word) | Q(name__icontains=word))
            total_counts = apartments.count()
    context = {
        'apartments': apartments,
        'count': total_counts,
    }
    return render(request, 'apartment/apartment.html', context)


