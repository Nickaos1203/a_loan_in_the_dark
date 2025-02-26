from django import forms
from accounts.models import CustomUser

class UserCreate(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'is_staff', 'username', 'phone_number', 'last_name', 'first_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
