from django.contrib import admin
from .models import Application, Transaction

admin.site.register(Application)
admin.site.register(Transaction)