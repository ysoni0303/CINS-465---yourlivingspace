from django.contrib import admin
from .models import Category

# Register your models here.
class CAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CAdmin)
