from django import forms
from .models import Account

class ProfileForm(forms.ModelForm):
     class Meta:
         model = Account
         fields = ('first_name', 'last_name', 'phone_number','address', 'zip_code', 'city', 'state')
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_pass = cleaned_data.get('confirm_pass')

        if password != confirm_pass:
            raise forms.ValidationError(
                "Password does not match!")


