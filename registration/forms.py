from django.forms import ModelForm
from django import forms
from .models import Instrument

# def select_validator(value):
#     if value == "Select Instrument":
#         raise forms.ValidationError('Please select your instument.')



class AttendeeForm(forms.Form):
    name = forms.CharField(max_length=100)
    qs = Instrument.objects.all()
    instrument = forms.ModelChoiceField(queryset=qs, empty_label="Select instrument")
    other_inst = forms.CharField(max_length=30, required=False)

class CreateProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300, widget=forms.Textarea)
    product_id = forms.CharField(max_length=100)