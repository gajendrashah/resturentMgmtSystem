from django import forms
from .models import Purchase, Customer, customerAdvance

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item_name', 'quantity', 'total_cost', 'bill_number', 'remarks']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'bill_number': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'room']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomerAdvanceForm(forms.ModelForm):
    class Meta:
        model = customerAdvance
        fields = ['customers', 'Advance', 'Payment_Method']
        widgets = {
            'customers': forms.Select(attrs={'class': 'form-control'}),
            'Advance': forms.NumberInput(attrs={'class': 'form-control'}),
            'Payment_Method': forms.Select(attrs={'class': 'form-control'}),
        }
