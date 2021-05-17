from django import forms


class add_form(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    value = forms.DecimalField(min_value=0)


class search_form(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    time = forms.CharField(max_length=255, label="Время", required=False)


class convert_form(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    currency2 = forms.CharField(max_length=5, label="Валюта")
    money = forms.DecimalField(min_value=0, label="Сумма")
    time = forms.CharField(max_length=255, label="Время", required=False)
