from django import forms
from news.models import New

class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'content']