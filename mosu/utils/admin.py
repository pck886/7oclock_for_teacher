from django.contrib import admin
from django import forms

# Register your models here.
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


