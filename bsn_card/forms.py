from django import forms
from .models import *


# class detailsForm(forms.ModelForm):
#     class Meta:
#         model = details
#         fields= ['img_bsn']
#         # fields= ['email_id',  'name', 'img_bsn', 'desc','Desi', 'Dept','phone_no', 'offer']
#         # fields ='__all__'
#         # labels={"img_bsn": ''}




class masterForm(forms.ModelForm):
    class Meta:
        model= master
        fields ='__all__'
        labels={"img":''}


# class masterForm1(forms.ModelForm):
#     class Meta:
#         model= master
#         fields ='__all__'
#         labels={"img":''}

class MasterForm1(forms.Form):
    # Your other form fields go here

    # Use FileField if you allow any file type, or ImageField if you only want images.
    # Make sure to install the 'Pillow' library for ImageField to work.
    image = forms.FileField()
