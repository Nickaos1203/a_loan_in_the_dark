from django import forms
from accounts.models import CustomUser

class UserCreate(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff']