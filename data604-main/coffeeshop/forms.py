from django import forms
from .models import Orders
from django.forms import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row


class CoffeeShopOrderForm(forms.ModelForm):
    # Generates quantity choices from 1 to 5
    quantity_choices = [('', '--')] + [(i, str(i)) for i in range(1, 6)]
    quantity = forms.ChoiceField(choices=quantity_choices, 
                                 initial=1,
                                 widget=forms.Select(attrs={'class': 'quantity-dropdown'}))
    
    
    def __init__(self, *args, **kwargs):
        super(CoffeeShopOrderForm, self).__init__(*args, **kwargs)

        self.fields['product'].widget.attrs.update({'data-product-id': 'id_product', 'style': 'font-size: 12px;'})
        self.fields['quantity'].widget.attrs.update({'class': 'quantity-field', 'style': 'font-size: 12px;'})
        self.fields['unit_price'].widget.attrs.update({'class': 'unit-price-field', 'readonly': 'readonly', 'style': 'font-size: 12px;'})
        self.fields['line_item_amount'].widget.attrs.update({'class': 'line-item-amount-field', 'readonly': 'readonly', 'style': 'font-size: 12px;'})
        self.fields['unit_price'].label = 'Price'
        self.fields['line_item_amount'].label = 'Total'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('product', css_class="col-md-5"),
                Column('quantity', css_class="col-md-2"),
                Column('unit_price', css_class="col-md-2"),
                Column('line_item_amount', css_class="col-md-2", readonly=True),
                Column(HTML('<button type="button" class="remove-form-row btn btn-danger">-</button>'),
                css_class="col-md-1 d-flex align-items-center"),
                )
            )

    class Meta:
        model = Orders
        fields = ['product', 'quantity', 'unit_price', 'line_item_amount']