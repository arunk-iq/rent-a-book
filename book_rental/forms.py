# forms.py
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
import json

class RentalForm(forms.Form):
    userId = forms.IntegerField()
    selectedBook = forms.JSONField(
        encoder=DjangoJSONEncoder,  # JSON encoder
        label="Selected Book"
    )
    rentedDate = forms.DateField()
    returnDate = forms.DateField()

