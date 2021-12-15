from django import forms
from .models import Review, Apartment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']
    
class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['name', 'description', 'rent', 'image', 'category' ]

class ApartmentFormForSaving(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['name','slug', 'description', 'rent', 'image', 'category' ]