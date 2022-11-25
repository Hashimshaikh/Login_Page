from django import forms
from app.models import pangresdata

class detailsform(forms.ModelForm):
    class Meta:
        model=pangresdata
        fields="__all__"