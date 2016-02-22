# In forms.py...
from django import forms
from .models import Attachment


class BasicUploadFileForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'id': 'fileupload', }
        )
    )

    class Meta:
        model = Attachment
        fields = ['file']
