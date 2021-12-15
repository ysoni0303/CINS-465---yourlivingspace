from django import forms
from .models import Application
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'state', 'city','status']
