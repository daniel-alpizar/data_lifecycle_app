from django import forms
from .models import Receipts

class CoffeeShopOrderForm(forms.ModelForm):
    class Meta:
        model = Receipts
        fields = ['product_id', 'quantity', 'unit_price']