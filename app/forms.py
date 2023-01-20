from django import forms
from .models import Order



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError(
                "The passwords you entered do not match. Please try again."
            )



class LoginForm(forms.Form):
    # campi per l'accesso
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['type', 'price', 'quantity']