from django import forms

class OrderForm(forms.Form):
    email = forms.EmailField(label='Enter email address', max_length=50, required=True)
    order_total = forms.FloatField(label='Enter order total', required=True)

class SearchForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=50)