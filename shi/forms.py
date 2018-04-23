from django import forms

from .models import Shi, Choice


class ShiForm(forms.ModelForm):

    class Meta:
        model = Shi
        fields = ('input_text',)

