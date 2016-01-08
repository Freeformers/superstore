from django import forms
from .models import Department, Product

SEARCH_COLOURS = [(0, '---'),] + Product.COLOURS

class ProductSearchForm(forms.Form):
    department = forms.ModelChoiceField(Department.objects.all(), required=False)
    name = forms.CharField(required=False)
    colour = forms.ChoiceField(choices=SEARCH_COLOURS, required=False)