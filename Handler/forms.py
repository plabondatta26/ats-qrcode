from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = QrCodeModel
        fields = '__all__'
