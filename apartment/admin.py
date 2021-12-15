from django.contrib import admin
from .models import Apartment, Review
# Register your models here.
class ApartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' :('name',)}

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Review)