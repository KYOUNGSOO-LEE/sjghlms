from django import forms
from .models import *


class BookForm(forms.Form):
    check1 = forms.BooleanField()
    check2 = forms.BooleanField()
    cls = forms.ModelChoiceField(queryset=Class.objects.all())
    period = forms.ModelChoiceField(queryset=Period.objects.all())
