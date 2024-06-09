from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'quantity_available']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'address', 'phone_number']

class BillForm(forms.ModelForm):
    PAID_CHOICES = [
        (True, 'Paid'),
        (False, 'Unpaid'),
    ]

    paid = forms.ChoiceField(choices=PAID_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Bill
        fields = ['customer', 'vat', 'shipping_cost', 'paid']

    def __init__(self, *args, **kwargs):
        update = kwargs.pop('update', False)
        super().__init__(*args, **kwargs)
        self.fields['vat'].widget.attrs['readonly'] = 'readonly'
        if update:
            self.fields['customer'].widget.attrs['readonly'] = 'readonly'
            self.fields['vat'].widget.attrs['readonly'] = 'readonly'
            self.fields['shipping_cost'].widget.attrs['readonly'] = 'readonly'
       


class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['product', 'quantity']
