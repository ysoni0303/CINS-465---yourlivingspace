from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def get_url(self):
            return reverse('apartments_by_category', args=[self.slug])

    def __str__(self):
        return self.name
