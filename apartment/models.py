from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.

class Apartment(models.Model):
    name            = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    rent           = models.IntegerField()
    image          = models.ImageField(upload_to='photos/apartments')
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def avg(self):
        avg = 0
        reviews = Review.objects.filter(apartment=self).aggregate(average=Avg('rating'))
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def totalReviewCount(self):
        c = 0
        reviews = Review.objects.filter(apartment=self).aggregate(count=Count('id'))
        if reviews['count'] is not None:
            c = int(reviews['count'])
        return c

    def get_url(self):
        return reverse('apartment_view', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name



class Review(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


