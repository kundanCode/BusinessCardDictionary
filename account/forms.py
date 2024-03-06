from django import forms
from .models import *


class detailsForm(forms.ModelForm):
    class Meta:
        model = details

        # fields= ['email_id',  'img_bsn', ]
        fields= ['email_id',  'name', 'img_bsn', 'desc','Desi', 'Dept','phone_no', 'offer']