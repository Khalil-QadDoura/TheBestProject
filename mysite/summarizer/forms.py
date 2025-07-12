from django import forms

class UploadForm(forms.Form):
    pdf_file = forms.FileField()
