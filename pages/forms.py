from django import forms

from .models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['name', 'url', 'enabled', 'expires', 'email']