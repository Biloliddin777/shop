from django import forms
from .models import Region, Customer
from .models import Purchase

# Форма для создания/редактирования региона
class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']  # Поля, которые должны быть в форме

# Форма для создания/редактирования покупателя
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'number', 'region']  # Поля, которые должны быть в форме



class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['customer', 'powder', 'quantity']
